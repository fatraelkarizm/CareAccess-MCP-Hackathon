import unittest

from gemini_generation import generate_prior_auth_draft


class GeminiGenerationTests(unittest.IsolatedAsyncioTestCase):
    async def test_generate_prior_auth_draft_returns_fallback_without_api_key(self):
        result = await generate_prior_auth_draft(
            decision={"treatment": "Semaglutide"},
            patient_summary="Synthetic patient",
            fallback_text="Fallback prior auth packet",
            api_key=None,
        )

        self.assertEqual(result, "Fallback prior auth packet")

    async def test_generate_prior_auth_draft_uses_injected_client_response(self):
        async def fake_client(prompt: str, api_key: str, model: str) -> str:
            self.assertIn("Semaglutide", prompt)
            self.assertEqual(api_key, "test-key")
            self.assertTrue(model)
            return "Gemini generated prior auth packet"

        result = await generate_prior_auth_draft(
            decision={"treatment": "Semaglutide"},
            patient_summary="Synthetic patient",
            fallback_text="Fallback prior auth packet",
            api_key="test-key",
            client=fake_client,
        )

        self.assertEqual(result, "Gemini generated prior auth packet")

    async def test_generate_prior_auth_draft_falls_back_when_client_fails(self):
        async def failing_client(prompt: str, api_key: str, model: str) -> str:
            raise RuntimeError("Gemini unavailable")

        result = await generate_prior_auth_draft(
            decision={"treatment": "Semaglutide"},
            patient_summary="Synthetic patient",
            fallback_text="Fallback prior auth packet",
            api_key="test-key",
            client=failing_client,
        )

        self.assertEqual(result, "Fallback prior auth packet")
