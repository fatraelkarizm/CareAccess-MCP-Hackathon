import unittest

from tools.coverage_tools import (
    assess_treatment_access,
    check_prior_auth,
    estimate_cost,
    explain_benefits,
    generate_prior_auth,
    suggest_alternatives,
    verify_coverage,
)


class CoverageToolsTests(unittest.IsolatedAsyncioTestCase):
    async def test_verify_coverage_returns_human_readable_decision(self):
        result = await verify_coverage(
            treatment="Semaglutide",
            plan="Acme Silver PPO",
            diagnosis="Type 2 Diabetes",
            clinical_context="A1C above goal after metformin trial",
        )

        self.assertIn("Coverage: covered_with_prior_auth", result)
        self.assertIn("Prior authorization required: yes", result)
        self.assertIn("Estimated patient cost: $75/month", result)

    async def test_check_prior_auth_returns_reason(self):
        result = await check_prior_auth(
            treatment="Semaglutide",
            plan="Acme Silver PPO",
            diagnosis="Type 2 Diabetes",
            clinical_context="A1C above goal after metformin trial",
        )

        self.assertIn("Prior authorization is required", result)
        self.assertIn("GLP-1", result)

    async def test_estimate_cost_returns_patient_cost(self):
        result = await estimate_cost(
            treatment="Semaglutide",
            plan="Acme Silver PPO",
        )

        self.assertIn("$75/month", result)

    async def test_suggest_alternatives_returns_covered_alternative(self):
        result = await suggest_alternatives(
            treatment="Semaglutide",
            plan="Acme Silver PPO",
        )

        self.assertIn("Metformin ER", result)

    async def test_generate_prior_auth_returns_packet(self):
        result = await generate_prior_auth(
            treatment="Semaglutide",
            plan="Acme Silver PPO",
            diagnosis="Type 2 Diabetes",
            patient_summary="Synthetic patient with Type 2 Diabetes",
            clinical_context="A1C above goal after metformin trial",
        )

        self.assertIn("Prior Authorization Draft", result)
        self.assertIn("Human Review Required", result)

    async def test_explain_benefits_returns_patient_friendly_summary(self):
        result = await explain_benefits(
            treatment="Semaglutide",
            plan="Acme Silver PPO",
        )

        self.assertIn("Your plan lists Semaglutide", result)
        self.assertIn("$75/month", result)

    async def test_assess_treatment_access_returns_showcase_brief(self):
        result = await assess_treatment_access(
            treatment="Semaglutide",
            plan="Acme Silver PPO",
            diagnosis="Type 2 Diabetes",
            patient_summary="Synthetic patient with Type 2 Diabetes",
            clinical_context="A1C above goal after metformin trial",
        )

        self.assertIn("CareAccess MCP Treatment Access Brief", result)
        self.assertIn("Coverage: covered_with_prior_auth", result)
        self.assertIn("Next best action", result)
        self.assertIn("Prior Authorization Draft", result)
        self.assertIn("Human Review Required", result)


if __name__ == "__main__":
    unittest.main()
