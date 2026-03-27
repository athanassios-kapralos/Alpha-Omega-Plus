"""
AΩ+ Reasoning Stability Field – Token‑level Implementation

This script computes for each sentence in a text file:
- gradient norm squared of the potential field Ψ
- estimated Laplacian (trace of Hessian) via Hutchinson estimator
- stability score S = ΔΨ - λ·‖∇Ψ‖²

It uses token embeddings from a sentence transformer (all-MiniLM-L6-v2)
and a uniform attention weight approximation (all pairs have equal weight).

Results are saved to a CSV and the top N most unstable sentences are plotted.
"""

# Requirements: pip install torch numpy sentence-transformers tqdm matplotlib seaborn

import torch
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import csv
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================================
# Configuration parameters
# ============================================================================
INPUT_FILE = "dataset.txt"                # one sentence per line
OUTPUT_CSV = "stability_scores_per_sentence.csv"
BATCH_SIZE = 8                            # number of sentences encoded together (adjust for GPU memory)
LAMBDA_STAB = 1.0                         # λ in S = ΔΨ - λ·‖∇Ψ‖²
M_HUTCHINSON = 5                          # number of random vectors for trace estimation
MAX_SEQ_LENGTH = 128                      # truncate/pad sentences to this many tokens
TOP_N_VISUAL = 20                         # number of most unstable sentences to plot

# ============================================================================
# Device setup
# ============================================================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# ============================================================================
# Load model (token embeddings)
# ============================================================================
model = SentenceTransformer('all-MiniLM-L6-v2', device=device)
model.max_seq_length = MAX_SEQ_LENGTH

def get_token_embeddings(texts):
    """
    Returns a list of token‑level embedding tensors for each text.
    Each tensor has shape (num_tokens, embedding_dim).
    """
    # encode returns a list of numpy arrays; convert to torch tensors on device
    token_emb_np = model.encode(texts, convert_to_tensor=False, output_value='token_embeddings')
    return [torch.tensor(emb, device=device) for emb in token_emb_np]

# ============================================================================
# Potential field Ψ (kernelized, uniform attention)
# ============================================================================
def pairwise_cosine_similarity(embeddings):
    """
    embeddings: (L, d)
    Returns (L, L) cosine similarity matrix.
    """
    norms = torch.norm(embeddings, dim=1, keepdim=True)
    embeddings_norm = embeddings / norms.clamp(min=1e-8)
    sim = torch.mm(embeddings_norm, embeddings_norm.t())
    return sim

def potential_field(embeddings, kernel='cosine'):
    """
    Ψ = Σ_{i<j} α_{i,j} · κ(e_i, e_j)
    Uses uniform α = 1/(L*(L-1)) for all pairs (i≠j).
    """
    L = embeddings.shape[0]
    if L < 2:
        return torch.tensor(0.0, device=embeddings.device, dtype=embeddings.dtype)
    if kernel == 'cosine':
        sim = pairwise_cosine_similarity(embeddings)
        sim = sim - torch.diag(torch.diag(sim))          # remove diagonal
        return sim.sum() / (L * (L - 1))
    else:
        raise NotImplementedError("Only cosine kernel is implemented.")

# ============================================================================
# Hutchinson trace estimator for Laplacian (ΔΨ)
# ============================================================================
def hutchinson_trace_laplacian(func, inputs, m=5):
    """
    Estimates trace of Hessian of func at inputs using Hutchinson's method.
    inputs: tensor (L, d) with requires_grad=True (will be set inside)
    Returns a float.
    """
    inputs.requires_grad_(True)
    outputs = func(inputs)               # scalar Ψ
    grads = torch.autograd.grad(outputs, inputs, create_graph=True)[0]  # ∇Ψ

    trace_est = 0.0
    for _ in range(m):
        v = torch.randn_like(inputs)               # random vector
        gv = torch.sum(grads * v)                  # ∇Ψ · v
        hv = torch.autograd.grad(gv, inputs, retain_graph=True)[0]  # H·v
        trace_est += torch.sum(v * hv).item()
    return trace_est / m

# ============================================================================
# Read all sentences
# ============================================================================
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    all_texts = [line.strip() for line in f if line.strip()]

print(f"Total sentences: {len(all_texts)}")

# ============================================================================
# Prepare CSV output
# ============================================================================
with open(OUTPUT_CSV, mode='w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(["text", "grad_norm_sq", "laplacian_est", "stability_score"])

# ============================================================================
# Main processing loop
# ============================================================================
top_entries = []  # list of (stability_score, text)

for start_idx in tqdm(range(0, len(all_texts), BATCH_SIZE), desc="Processing"):
    batch_texts = all_texts[start_idx:start_idx + BATCH_SIZE]
    batch_token_embs = get_token_embeddings(batch_texts)   # list of (L_i, d)

    for idx, emb in enumerate(batch_token_embs):
        text = batch_texts[idx]
        L = emb.shape[0]

        if L < 2:
            # Not enough tokens to form pairs -> Ψ = 0, no meaningful stability
            grad_norm_sq = 0.0
            laplacian_est = 0.0
            stability = 0.0
        else:
            # Define a closure that computes Ψ for this sentence's embeddings
            def psi_func(x):
                return potential_field(x, kernel='cosine')

            # Clone with gradient tracking
            x = emb.clone().detach().requires_grad_(True)

            # Gradient norm squared
            psi = psi_func(x)
            psi.backward()
            grad_norm_sq = torch.sum(x.grad ** 2).item()

            # Laplacian estimate
            laplacian_est = hutchinson_trace_laplacian(psi_func, x, m=M_HUTCHINSON)

            # Stability score
            stability = laplacian_est - LAMBDA_STAB * grad_norm_sq

        # Write to CSV
        with open(OUTPUT_CSV, mode='a', newline='', encoding='utf-8-sig') as f_out:
            writer = csv.writer(f_out)
            writer.writerow([text, grad_norm_sq, laplacian_est, stability])

        # Update top N most unstable (lowest stability score)
        top_entries.append((stability, text))
        top_entries.sort(key=lambda x: x[0])               # ascending: most unstable first
        top_entries = top_entries[:TOP_N_VISUAL]

print(f"Computation finished. Results saved to {OUTPUT_CSV}")

# ============================================================================
# Visualisation: bar plot of the most unstable sentences
# ============================================================================
top_texts = [entry[1] for entry in top_entries]
top_scores = [entry[0] for entry in top_entries]

plt.figure(figsize=(12, 6))
sns.barplot(x=[t[:50] + "..." for t in top_texts], y=top_scores, palette="coolwarm")
plt.title(f"Top {len(top_entries)} Lowest Stability Scores (most unstable sentences)")
plt.ylabel("Stability score (lower = more unstable)")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
