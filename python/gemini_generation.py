import os
from typing import Awaitable, Callable

import httpx


GeminiClient = Callable[[str, str, str], Awaitable[str]]

GEMINI_GENERATE_CONTENT_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
)
DEFAULT_GEMINI_MODEL = "gemini-2.0-flash"


def _build_prior_auth_prompt(decision: dict, patient_summary: str) -> str:
    return f"""Create a concise, reviewable prior authorization draft for a healthcare administrator.

Use only the structured information below. Do not invent payer facts, diagnoses,
or clinical details. Include a clear human-review disclaimer.

Patient summary:
{patient_summary}

Coverage decision:
{decision}
"""


async def _call_gemini_generate_content(prompt: str, api_key: str, model: str) -> str:
    url = GEMINI_GENERATE_CONTENT_URL.format(model=model)
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt,
                    }
                ]
            }
        ]
    }

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.post(
            url,
            headers={"x-goog-api-key": api_key},
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

    candidates = data.get("candidates") or []
    if not candidates:
        raise RuntimeError("Gemini returned no candidates")

    parts = candidates[0].get("content", {}).get("parts") or []
    text = "".join(part.get("text", "") for part in parts).strip()
    if not text:
        raise RuntimeError("Gemini returned an empty text response")

    return text


async def generate_prior_auth_draft(
    decision: dict,
    patient_summary: str,
    fallback_text: str,
    api_key: str | None = None,
    model: str | None = None,
    client: GeminiClient = _call_gemini_generate_content,
) -> str:
    api_key = api_key if api_key is not None else os.getenv("GEMINI_API_KEY")
    model = model or os.getenv("GEMINI_MODEL") or DEFAULT_GEMINI_MODEL

    if not api_key:
        return fallback_text

    prompt = _build_prior_auth_prompt(decision=decision, patient_summary=patient_summary)
    try:
        return await client(prompt, api_key, model)
    except Exception:
        return fallback_text
