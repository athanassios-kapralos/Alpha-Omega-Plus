"""
AΩ+ Justice & Ethical Stability Module
Implements Golden Ratio (Φ) harmony between individual rights and collective good.
"""

def evaluate_justice(individual_rights, collective_good, return_warning=False):
    """
    Returns a stability score for justice/ethics using Golden Ratio harmony.

    Parameters:
        individual_rights (float): Score representing individual rights (0..1 or scaled)
        collective_good (float): Score representing collective good (0..1 or scaled)
        return_warning (bool): If True, returns (score, warning_string) instead of just score

    Returns:
        float or tuple: Justice score (0..1, higher = better balance).
        If return_warning is True, also returns a warning string for extreme imbalances.
    """
    phi = 1.618033988749895  # Golden Ratio

    # Avoid division by zero (add small epsilon)
    denominator = collective_good + 1e-9
    harmony_point = individual_rights / denominator

    # --- Edge-case warnings (extreme imbalances) ---
    warning = None
    if harmony_point > 5 * phi:
        warning = "Tyranny of the Individual"
    elif harmony_point < phi / 5:
        warning = "Oppression of the Individual"

    # Tension: how far the harmony point deviates from Φ
    tension = abs(harmony_point - phi)
    # Truth score: inverse of tension (capped to [0,1])
    truth_score = 1 / (1 + tension)

    if return_warning:
        return round(truth_score, 4), warning
    return round(truth_score, 4)


# --- Example usage and test ---
if __name__ == "__main__":
    # Balanced case (individual rights : collective good ≈ Φ)
    balanced_score, warn = evaluate_justice(0.8, 0.494, return_warning=True)
    print(f"Balanced: score = {balanced_score}, warning = {warn}")

    # Extreme cases
    tyranny_score, warn_tyranny = evaluate_justice(10.0, 0.1, return_warning=True)
    print(f"Tyranny: score = {tyranny_score}, warning = {warn_tyranny}")

    oppression_score, warn_oppression = evaluate_justice(0.1, 10.0, return_warning=True)
    print(f"Oppression: score = {oppression_score}, warning = {warn_oppression}")

    # Standard usage (no warning)
    print(f"Default: {evaluate_justice(0.8, 0.5)}")
