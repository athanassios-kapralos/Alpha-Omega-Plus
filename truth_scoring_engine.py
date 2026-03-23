"""
AΩ+ Truth Scoring Engine (Wrapper)
This is a lightweight wrapper around the official 12‑dimensional evaluator.
For full functionality, see `truth_evaluator.py`.
"""

from truth_evaluator import AO_TruthEvaluator

def evaluate_12d(raw_values, domain="default"):
    """
    Evaluate a set of raw dimension scores (D1‑D12) using the AΩ+ 12‑dimensional
    truth evaluator.

    Parameters:
        raw_values (dict): Keys D1_Nominal, D2_Conceptual, ..., D12_Logical.
        domain (str): "scientific", "ethical", "definitional", or "default".

    Returns:
        dict: Same output as AO_TruthEvaluator.evaluate_12d.
    """
    evaluator = AO_TruthEvaluator()
    return evaluator.evaluate_12d(raw_values, domain)
