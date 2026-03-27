"""
AΩ+ Reasoning Stability Field – Production‑Ready Version

Implements the reasoning potential field Ψ with token embeddings,
gradient norm, and Hutchinson‑estimated Laplacian.
Keeps top N most unstable sentences using a max‑heap of negated scores.

All known issues resolved:
- Correct heap logic (max‑heap of negated stability scores).
- Hutchinson estimator clones input to avoid side effects.
- CSV opened once.
- functools.partial used for kernel function to avoid closure pitfalls.
"""

import torch
import heapq
import functools
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import csv
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================================
# Configuration
# ============================================================================
INPUT_FILE = "dataset.txt"
OUTPUT_CSV = "stability_scores_per_sentence.csv"
BATCH_SIZE = 8
LAMBDA_STAB = 1.0
M_HUTCHINSON = 20
MAX_SEQ_LENGTH = 128
TOP_N_VISUAL = 20
SAVE_PLOT = "stability_top.png"

# ============================================================================
# Device
# ============================================================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# ============================================================================
# Model (token embeddings)
# ============================================================================
model = SentenceTransformer('all-MiniLM-L6-v2', device=device)
model.max_seq_length = MAX_SEQ_LENGTH

def get_token_embeddings(texts):
    token_emb_np = model.encode(texts, convert_to_tensor=False, output_value='token_embeddings')
    return [torch.tensor(emb, device=device) for emb in token_emb_np]

# ============================================================================
# Potential field functions
# ============================================================================
def pairwise_cosine_similarity(embeddings):
    norms = torch.norm(embeddings, dim=1, keepdim=True)
    embeddings_norm = embeddings / norms.clamp(min=1e-8)
    return torch.mm(embeddings_norm, embeddings_norm.t())

def potential_field(embeddings, kernel='cosine'):
    L = embeddings.shape[0]
    if L < 2:
        return torch.tensor(0.0, device=embeddings.device, dtype=embeddings.dtype)
    if kernel == 'cosine':
        sim = pairwise_cosine_similarity(embeddings)
        sim = sim - torch.diag(torch.diag(sim))
        return sim.sum() / (L * (L - 1))
    else:
        raise NotImplementedError("Only cosine kernel is implemented.")

# ============================================================================
# Hutchinson trace estimator (safe)
# ============================================================================
def hutchinson_trace_laplacian(func, inputs, m=20):
    """
    Estimates trace of Hessian of func at inputs.
    Clones inputs to avoid side effects.
    """
    x = inputs.clone().detach().requires_grad_(True)
    outputs = func(x)
    grads = torch.autograd.grad(outputs, x, create_graph=True)[0]

    trace_est = 0.0
    for _ in range(m):
        v = torch.randn_like(x)
        gv = torch.sum(grads * v)
        hv = torch.autograd.grad(gv, x, retain_graph=True)[0]
        trace_est += torch.sum(v * hv).item()
    return trace_est / m

# ============================================================================
# Pre‑bind kernel to avoid closure in loop
# ============================================================================
psi_func = functools.partial(potential_field, kernel='cosine')

# ============================================================================
# Main
# ============================================================================
# Read all sentences
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    all_texts = [line.strip() for line in f if line.strip()]
print(f"Total sentences: {len(all_texts)}")

# Prepare CSV
with open(OUTPUT_CSV, mode='w', newline='', encoding='utf-8-sig') as f_csv:
    writer = csv.writer(f_csv)
    writer.writerow(["text", "grad_norm_sq", "laplacian_est", "stability_score"])

    # Max‑heap to keep top N most unstable (lowest stability)
    # Stores (-stability, text) so that heap root is the largest -stability,
    # which corresponds to the smallest (most unstable) stability.
    top_heap = []

    for start_idx in tqdm(range(0, len(all_texts), BATCH_SIZE), desc="Processing"):
        batch_texts = all_texts[start_idx:start_idx + BATCH_SIZE]
        batch_token_embs = get_token_embeddings(batch_texts)

        for idx, emb in enumerate(batch_token_embs):
            text = batch_texts[idx]
            L = emb.shape[0]

            if L < 2:
                grad_norm_sq = 0.0
                laplacian_est = 0.0
                stability = 0.0
            else:
                # Gradient norm squared
                x = emb.clone().detach().requires_grad_(True)
                psi = psi_func(x)
                psi.backward()
                grad_norm_sq = torch.sum(x.grad ** 2).item()

                # Laplacian estimate (safe: clones inside)
                laplacian_est = hutchinson_trace_laplacian(psi_func, emb, m=M_HUTCHINSON)

                stability = laplacian_est - LAMBDA_STAB * grad_norm_sq

            # Write to CSV
            writer.writerow([text, grad_norm_sq, laplacian_est, stability])

            # Maintain heap of top N most unstable
            entry = (-stability, text)
            if len(top_heap) < TOP_N_VISUAL:
                heapq.heappush(top_heap, entry)
            else:
                # If current -stability is larger than the heap root (i.e., stability is smaller),
                # replace the root with this more unstable sentence.
                if -stability > top_heap[0][0]:
                    heapq.heapreplace(top_heap, entry)

    # After processing, heap contains the TOP_N_VISUAL most unstable sentences.
    # Convert back to positive stability and sort ascending.
    top_entries = sorted([(-s, t) for s, t in top_heap], key=lambda x: x[0])

print(f"Computation finished. Results saved to {OUTPUT_CSV}")

# ============================================================================
# Visualization
# ============================================================================
top_texts = [entry[1] for entry in top_entries]
top_scores = [entry[0] for entry in top_entries]

plt.figure(figsize=(12, 6))
sns.barplot(x=[t[:50] + "..." for t in top_texts], y=top_scores, palette="coolwarm")
plt.title(f"Top {len(top_entries)} Lowest Stability Scores (most unstable sentences)")
plt.ylabel("Stability score (lower = more unstable)")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(SAVE_PLOT, dpi=150)
plt.show()
