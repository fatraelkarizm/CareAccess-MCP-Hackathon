import unittest

from insurance_rules import (
    generate_prior_auth_packet,
    get_coverage_decision,
)


class InsuranceRulesTests(unittest.TestCase):
    def test_semaglutide_requires_prior_auth_and_returns_cost(self):
        decision = get_coverage_decision(
            treatment="Semaglutide",
            plan="Acme Silver PPO",
            diagnosis="Type 2 Diabetes",
            clinical_context="A1C above goal after metformin trial",
        )

        self.assertEqual(decision["coverage"], "covered_with_prior_auth")
        self.assertTrue(decision["prior_auth_required"])
        self.assertEqual(decision["estimated_patient_cost"], "$75/month")
        self.assertEqual(decision["covered_alternative"], "Metformin ER")
        self.assertIn("GLP-1", decision["reason"])

    def test_unknown_treatment_returns_not_found_decision(self):
        decision = get_coverage_decision(
            treatment="Experimental Therapy",
            plan="Acme Silver PPO",
            diagnosis="Type 2 Diabetes",
            clinical_context="No matching payer rule",
        )

        self.assertEqual(decision["coverage"], "unknown")
        self.assertFalse(decision["prior_auth_required"])
        self.assertIn("No synthetic payer rule", decision["reason"])

    def test_lumbar_mri_requires_prior_auth_with_imaging_documentation(self):
        decision = get_coverage_decision(
            treatment="Lumbar Spine MRI",
            plan="Acme Silver PPO",
            diagnosis="Low back pain with radiculopathy",
            clinical_context="Persistent symptoms after conservative therapy",
        )

        self.assertEqual(decision["coverage"], "covered_with_prior_auth")
        self.assertTrue(decision["prior_auth_required"])
        self.assertEqual(decision["estimated_patient_cost"], "$150 imaging copay")
        self.assertIn("conservative therapy", decision["reason"])
        self.assertIn("Neurologic exam findings", decision["documentation_required"])

    def test_hba1c_lab_is_covered_without_prior_auth(self):
        decision = get_coverage_decision(
            treatment="HbA1c Lab",
            plan="Acme Silver PPO",
            diagnosis="Type 2 Diabetes",
            clinical_context="Routine diabetes monitoring",
        )

        self.assertEqual(decision["coverage"], "covered")
        self.assertFalse(decision["prior_auth_required"])
        self.assertEqual(decision["estimated_patient_cost"], "$0 preventive lab benefit")

    def test_wegovy_for_weight_loss_is_not_covered(self):
        decision = get_coverage_decision(
            treatment="Wegovy",
            plan="Acme Silver PPO",
            diagnosis="Weight management",
            clinical_context="No diabetes diagnosis documented",
        )

        self.assertEqual(decision["coverage"], "not_covered")
        self.assertFalse(decision["prior_auth_required"])
        self.assertEqual(decision["estimated_patient_cost"], "full retail cost")
        self.assertIn("weight-loss medications", decision["reason"])

    def test_prior_auth_packet_includes_reviewable_sections(self):
        decision = get_coverage_decision(
            treatment="Semaglutide",
            plan="Acme Silver PPO",
            diagnosis="Type 2 Diabetes",
            clinical_context="A1C above goal after metformin trial",
        )

        packet = generate_prior_auth_packet(
            patient_summary="Synthetic patient with Type 2 Diabetes",
            decision=decision,
        )

        self.assertIn("Prior Authorization Draft", packet)
        self.assertIn("Semaglutide", packet)
        self.assertIn("Clinical Rationale", packet)
        self.assertIn("Human Review Required", packet)


if __name__ == "__main__":
    unittest.main()
