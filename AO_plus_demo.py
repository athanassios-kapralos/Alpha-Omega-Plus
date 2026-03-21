"""
ΑΩ+ (Alpha-Omega Plus) Research Demo
Integrates Truth Evaluation, Tetralectic Gate, Harmonic Scaling, and Justice Score
Author: Athanassios Kapralos
"""

PHI = 1.618033988749895

# -------------------------------
# Truth Evaluation & Harmonic Scaling
# -------------------------------
def evaluate_truth(dimensions, truth_values, weights):
    if len(dimensions) != len(truth_values) or len(truth_values) != len(weights):
        raise ValueError("Dimensions, truth values, and weights must match in length.")
    
    truth_score = sum(w * t for w, t in zip(weights, truth_values))
    mean = sum(truth_values) / len(truth_values)
    variance = sum((t - mean) ** 2 for t in truth_values) / len(truth_values)
    consistency = 1 - (variance ** 0.5)
    
    return round(truth_score, 4), round(consistency, 4)

def adjust_harmonic_scaling(N, truth_score, threshold=0.7):
    if truth_score < threshold:
        return round(N * (1 + (threshold - truth_score)), 2)
    return N

# -------------------------------
# Tetralectic Gate
# -------------------------------
def tetralectic_gate(statement, evaluator):
    poles = {
        'θ': evaluator(statement),
        '/': evaluator(f"NOT: {statement}"),
        '§': evaluator(f"SIMILAR BUT WRONG: {statement}"),
        '~': evaluator(f"HARMONIOUS ALT: {statement}")
    }
    
    kl_harmony = abs(poles['θ'] - poles['~']) < 0.2
    kk_harmony = abs(poles['/'] - poles['§']) < 0.2
    
    truth_score = ((poles['θ'] + poles['~']) / 2) * (1 / PHI)
    passed_fire = kl_harmony and kk_harmony
    
    return {"score": round(min(truth_score, 1.0), 4), "passed": passed_fire, "poles": poles}

# Example evaluator function
def simple_evaluator(statement):
    """
    Heuristic evaluator: rewards nuance, penalizes absolutes.
    """
    score = 0.8
    traps = ["always", "never", "must", "impossible"]
    boosters = ["however", "evidence", "suggests", "research shows"]
    
    stmt = statement.lower()
    for t in traps:
        if t in stmt:
            score -= 0.1
    for b in boosters:
        if b in stmt:
            score = min(1.0, score + 0.05)
    if len(stmt) < 15 or len(stmt) > 600:
        score -= 0.1
    return max(0.1, round(score, 2))

# -------------------------------
# Justice & Ethical Score
# -------------------------------
def evaluate_justice(individual_rights, collective_good):
    phi = 1.618033
    harmony_point = individual_rights / collective_good
    tension = abs(harmony_point - phi)
    truth_score = 1 / (1 + tension)
    return round(truth_score, 4)

# -------------------------------
# Demo Execution
# -------------------------------
if __name__ == "__main__":
    # Truth Evaluation Example
    dimensions = ["logic", "evidence", "ethics"]
    truth_values = [0.9, 0.85, 0.95]
    weights = [0.4, 0.3, 0.3]
    
    score, consistency = evaluate_truth(dimensions, truth_values, weights)
    print("--- AΩ+ Truth Evaluation ---")
    print(f"Score: {score}, Consistency: {consistency}")
    
    N_initial = 10
    adjusted_N = adjust_harmonic_scaling(N_initial, score)
    print(f"Original Difficulty (N): {N_initial}, Adjusted Difficulty: {adjusted_N}")
    
    # Tetralectic Gate Example
    statement = "AI must enhance user experience while preserving privacy."
    tet_result = tetralectic_gate(statement, simple_evaluator)
    print("\n--- Tetralectic Gate ---")
    print(f"Score: {tet_result['score']}, Passed Fire: {tet_result['passed']}")
    print(f"Poles: {tet_result['poles']}")
    
    # Justice & Ethical Score Example
    justice_score = evaluate_justice(0.8, 0.494)
    print("\n--- Justice & Ethical Stability ---")
    print(f"Justice Score: {justice_score}")
