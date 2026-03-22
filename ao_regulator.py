import torch
from ao_regulator import AlphaOmegaRegulator

def test_regulator_behavior():
    # 1. Initialize with a high lambda for clear numerical results
    reg = AlphaOmegaRegulator(lambda_factor=1.0)
    
    # 2. STEP 1: High-Entropy Logits (Uncertain state)
    uncertain_logits = torch.ones(1, 100) 
    
    # 3. STEP 2: Low-Entropy Logits (Confident state)
    confident_logits = torch.zeros(1, 100)
    confident_logits[0, 0] = 20.0 

    print("--- Running AΩ+ Physical Logic Test ---")
    
    # Initial forward: last_entropy is None -> nabla_psi should be near zero
    p1 = reg(uncertain_logits)
    print(f"Step 1 (Initial Uncertain): Penalty = {p1.item():.4f}")
    
    # Second forward: Sharp drop in entropy -> nabla_psi should be negative
    p2 = reg(confident_logits)
    print(f"Step 2 (Transition to Confident): Penalty = {p2.item():.4f}")
    
    # 4. STEP 3: Return to Uncertainty -> nabla_psi should be positive
    p3 = reg(uncertain_logits)
    print(f"Step 3 (Return to Uncertainty): Penalty = {p3.item():.4f}")

    # Robust Assertions (using 1e-6 tolerance for float safety)
    assert abs(p1.item()) < 1e-6, "Initial step must have near-zero penalty."
    assert p2.item() < -0.1, "Entropy drop must result in significant negative field pressure."
    assert p3.item() > 0.1, "Entropy rise must result in significant positive field pressure."
    
    print("\n--- Test Passed: Field Dynamics Operational and Robust ---")

if __name__ == "__main__":
    test_regulator_behavior()
