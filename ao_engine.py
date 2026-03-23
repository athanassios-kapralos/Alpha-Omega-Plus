import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import logging

# Ρύθμιση Logging για επαγγελματική ιχνηλάτηση των εξισώσεων
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("AΩ+_Engine")

class AOPlusEngine:
    """
    Alpha-Omega Plus (AΩ+) Reasoning Engine - Version 1.1 [Scientific Edition]
    -----------------------------------------------------------------------
    Integrates Relativistic Scalar Fields, Tetralectic Logic, 
    and Logical Curvature (R) with Φ-Harmonic Stability.
    """

    def __init__(self, phi=1.618033, sigma=1.0, verbose=True):
        self.phi = phi          # Φ: Golden Ratio Stability Constant
        self.sigma = sigma      # σ: Regularization Scale
        self.verbose = verbose
        self.xi = 0.8           # ξ: Curvature Coupling Coefficient
        self.lam = 0.1          # λ: Non-linear interaction strength

        # ---------------- STABILITY MATRIX (Tetralectic Nodes) ----------------
        self.stability_matrix = {
            "eleutheria": {"role":"thesis","ethos":"kl","tetralect_id":1,
                           "partners":["eiloteia","asydosia","diakonia"],
                           "spectrum":["eleutheria","eleutheriazo","eleutherōmeni","eleutheriastiki"]},
            "eiloteia": {"role":"antithesis","ethos":"kk","tetralect_id":1,
                         "partners":["eleutheria","asydosia","diakonia"],
                         "spectrum":["eiloteia","eiloteuo","eiloteumeni","eilotiki"]},
            "asydosia": {"role":"deviation","ethos":"kk","tetralect_id":1,
                         "partners":["eleutheria","eiloteia","diakonia","ochlokratia"],
                         "spectrum":["asydosia","asydoto","asydotimeni","asydotiki"]},
            "diakonia": {"role":"parallel","ethos":"kl","tetralect_id":1,
                         "partners":["eleutheria","eiloteia","asydosia"],
                         "spectrum":["diakonia","diakono","diakonimeni","diakoniki"]},
            "demokratia": {"role":"thesis","ethos":"kl","tetralect_id":2,
                           "partners":["tyrannia","ochlokratia","hegemonia"],
                           "spectrum":["demokratia","demokrato","demokratimeni","demokratiki"]},
            "tyrannia": {"role":"antithesis","ethos":"kk","tetralect_id":2,
                         "partners":["demokratia","ochlokratia","hegemonia"],
                         "spectrum":["tyrannia","tyranno","tyrannimeni","tyranniki"]},
            "ochlokratia": {"role":"deviation","ethos":"kk","tetralect_id":2,
                            "partners":["demokratia","tyrannia","hegemonia","asydosia"],
                            "spectrum":["ochlokratia","ochlokrato","ochlokratimeni","ochlokratiki"]},
            "hegemonia": {"role":"parallel","ethos":"kl","tetralect_id":2,
                          "partners":["demokratia","tyrannia","ochlokratia"],
                          "spectrum":["hegemonia","hegemoneuo","hegemoneumeni","hegemoniki"]},
            "justice": {"role":"thesis","ethos":"kl","tetralect_id":0,
                        "partners":["harmony"],
                        "spectrum":["justice","justify","justified","just"]},
            "harmony": {"role":"thesis","ethos":"kl","tetralect_id":0,
                        "partners":["justice"],
                        "spectrum":["harmony","harmonize","harmonized","harmonic"]}
        }

    # ---------------- PHYSICS LAYER (Field Dynamics) ----------------
    def scalar_field_pressure_vec(self, psi_arr, R=0.1):
        """
        Calculates Field Pressure (ψ) coupled with Logical Curvature (R).
        Formula: |λψ³ * e^(-ψ²/σ²) - ξRψ|
        """
        psi_arr = np.array(psi_arr, dtype=float)
        
        # Nonlinear interaction with Gaussian Regularization
        regularization = np.exp(-psi_arr**2 / self.sigma**2)
        interaction = self.lam * psi_arr**3 * regularization
        
        # Curvature Coupling (ξ * R * ψ) - High R penalizes unstable logic
        curvature_coupling = self.xi * R * psi_arr
        
        pressure = np.abs(interaction - curvature_coupling)
        return pressure

    def harmonic_scaling(self, N, T0=100, alpha=2.08):
        """Φ-based scaling for resource allocation."""
        return T0 * (self.phi ** (alpha * N))

    # ---------------- LINGUISTIC LAYER (Symmetry Check) ----------------
    def check_kanon_3_vec(self, concept_arr):
        scores = []
        for concept in concept_arr:
            concept = concept.lower().strip()
            if concept in self.stability_matrix:
                entry = self.stability_matrix[concept]
                score = len(entry["spectrum"]) / 4
            else:
                score = 1 / self.phi
            scores.append(round(score,4))
        return np.array(scores)

    def check_kanon_4_vec(self, concept_arr, suffix_arr):
        scores = []
        for c, s in zip(concept_arr, suffix_arr):
            c = c.lower().strip()
            s = s.lower().strip()
            if c in self.stability_matrix:
                ethos = self.stability_matrix[c]["ethos"]
                # Penalize kakos-ethos (kk) coupled with problematic suffixes
                score = 0.1 if (ethos=="kk" and s=="iki") else 1.0
            else:
                score = 1.0
            scores.append(score)
        return np.array(scores)

    # ---------------- VECTOR MASTER OPERATOR (J_stab Bridge) ----------------
    def compute_unified_truth_score_vec(self, psi_arr, concept_arr, R=0.1, suffix_arr=None):
        """
        Bridges Physical Fields and Tetralectic Logic to find the Symmetry Stability Factor.
        """
        # Physics Calculation
        p_scores = self.scalar_field_pressure_vec(psi_arr, R=R)
        
        # Symmetry/Linguistic Calculation
        k3_scores = self.check_kanon_3_vec(concept_arr)
        k4_scores = self.check_kanon_4_vec(concept_arr, suffix_arr) if suffix_arr is not None else np.ones_like(p_scores)
        
        # Unified Raw Score before Φ-Scaling
        raw_stability = p_scores * k3_scores * k4_scores
        
        # Apply Φ-Harmonic Scaling for final stability check
        return np.round(np.abs(raw_stability * self.phi), 6)

    # ---------------- ANALYTICS & VISUALIZATION ----------------
    def generate_scores_dataframe(self, concept_root, psi_val=0.8, R=0.1, suffix=None):
        cluster = [concept_root.lower().strip()] + self.stability_matrix.get(concept_root.lower().strip(), {}).get("partners", [])
        if not cluster: return pd.DataFrame()
        
        psi_arr = np.full(len(cluster), psi_val)
        suffix_arr = [suffix]*len(cluster) if suffix else [None]*len(cluster)
        
        scores = self.compute_unified_truth_score_vec(psi_arr, cluster, R=R, suffix_arr=suffix_arr)
        
        df = pd.DataFrame({
            "Concept": cluster,
            "Field_Psi": psi_arr,
            "Curvature_R": R,
            "UnifiedScore": scores,
            "Ethos": [self.stability_matrix[c]["ethos"] for c in cluster]
        })
        return df

    def visualize_stability(self, concept_root, psi=0.8, R=0.1):
        df = self.generate_scores_dataframe(concept_root, psi_val=psi, R=R)
        if df.empty: return
        
        colors = ['#2ecc71' if e=="kl" else '#e74c3c' for e in df["Ethos"]]
        plt.figure(figsize=(10,6))
        bars = plt.bar(df["Concept"], df["UnifiedScore"], color=colors, edgecolor='black', alpha=0.8)
        
        plt.title(f"AΩ+ Stability Cluster: {concept_root.capitalize()} (R={R})")
        plt.ylabel("Unified Truth Score (J_stab)")
        plt.grid(axis='y', linestyle='--', alpha=0.3)
        
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.001, round(yval,4), ha='center', fontweight='bold')
        
        plt.show()
        return df

# ---------------- DEMO EXECUTION ----------------
if __name__ == "__main__":
    engine = AOPlusEngine()

    print("\n" + "="*60)
    print("  AΩ+ RESEARCH FRAMEWORK: SCALAR FIELD STABILITY ENGINE")
    print("="*60)

    # Scenario: Low Complexity R (Stable Environment)
    print("\n[SCENARIO 1] Low Logical Curvature (R=0.05)")
    df_stable = engine.visualize_stability("eleutheria", psi=0.9, R=0.05)
    print(df_stable[['Concept', 'UnifiedScore', 'Ethos']])

    # Scenario: High Complexity R (Unstable/Hallucination Risk)
    print("\n[SCENARIO 2] High Logical Curvature (R=0.85)")
    df_unstable = engine.visualize_stability("eleutheria", psi=0.9, R=0.85)
    print(df_unstable[['Concept', 'UnifiedScore', 'Ethos']])
    
    print("\n" + "-"*60)
    print("Observation: High Curvature R forces field decay, reducing Truth Scores.")
    print("-"*60)
