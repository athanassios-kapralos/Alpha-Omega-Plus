import math


class AOPlusEngine:
    """
    The Alpha-Omega Plus (AΩ+) Reasoning Engine.

    Conceptual engine that combines:
    - Scalar-field inspired stabilization
    - Tetralectic linguistic symmetry rules
    """

    def __init__(self, phi=1.618033, sigma=1.0):
        # Golden ratio (harmonic attractor)
        self.phi = phi

        # Normalization constant for the scalar field
        self.sigma = sigma

        # Stability matrix derived from the Tetralectic framework
        # Defines whether a concept has a complete linguistic spectrum
        self.stability_matrix = {
            "justice": ["justice", "justify", "justified", "just"],
            "harmony": ["harmony", "harmonize", "harmonized", "harmonic"],
            "diakonia": ["diakonia", "diakono", "diakonimeni", "diakoniki"],
            "hegemonia": ["hegemonia", "hegemoneuo", "hegemoneumeni", "hegemoniki"],
            "asydosia": ["asydosia", "asydoto", "asydotimeni", "asydotiki"],
            "tyrannia": ["tyrannia", "tyranno", "tyrannimeni", "tyranniki"]
        }

    def harmonic_scaling(self, N, T0=100, alpha=2.08):
        """
        Computes token budget based on problem complexity.

        Parameters
        ----------
        N : float
            Logical complexity level
        T0 : int
            Base token budget
        alpha : float
            Scaling coefficient
        """
        return T0 * (self.phi ** (alpha * N))

    def scalar_field_pressure(self, psi, lam=0.1):
        """
        Scalar field stabilization term.

        psi : float
            Field value representing reasoning flow
        lam : float
            Non-linear interaction coefficient
        """
        exponent = -(psi ** 2) / (self.sigma ** 2)
        return lam * (psi ** 3) * math.exp(exponent)

    def check_kanon_3(self, concept_root):
        """
        Canon 3: Linguistic spectrum validation.

        Returns
        -------
        1.0 if the concept has a complete lexical spectrum
        1/phi otherwise
        """
        concept = concept_root.lower()

        if concept in self.stability_matrix:
            return 1.0

        return round(1 / self.phi, 4)

    def check_kanon_4(self, concept_root, suffix):
        """
        Canon 4: Suffix trap detection.

        Certain negative roots cannot logically produce
        adjectival forms ending in '-iki'.
        """

        negative_roots = ["asydosia", "tyrannia"]

        if concept_root.lower() in negative_roots and suffix == "iki":
            return 0.1  # critical failure

        return 1.0

    def compute_unified_truth_score(self, psi, concept, current_suffix=None):
        """
        Central operator combining physics and tetralectic logic.

        Returns a stability-based truth probability.
        """

        # Physics-level score
        p_score = self.scalar_field_pressure(psi)

        # Linguistic symmetry scores
        k3_score = self.check_kanon_3(concept)
        k4_score = self.check_kanon_4(concept, current_suffix) if current_suffix else 1.0

        # Unified stability product
        final_stability = p_score * k3_score * k4_score

        return round(abs(final_stability), 6)


# ---------------------------------------------------------
# Example Usage
# ---------------------------------------------------------

if __name__ == "__main__":

    engine = AOPlusEngine()

    # Example 1: harmonic token scaling
    complexity = 3
    tokens = engine.harmonic_scaling(complexity)

    # Example 2: scalar field stabilization
    psi_value = 0.8
    pressure = engine.scalar_field_pressure(psi_value)

    # Example 3: tetralectic linguistic validation
    kanon3 = engine.check_kanon_3("justice")
    kanon4 = engine.check_kanon_4("tyrannia", "iki")

    # Example 4: unified truth score
    truth_score = engine.compute_unified_truth_score(
        psi=0.8,
        concept="justice"
    )

    print("Token Budget:", tokens)
    print("Scalar Pressure:", pressure)
    print("Kanon 3:", kanon3)
    print("Kanon 4:", kanon4)
    print("Unified Truth Score:", truth_score)
