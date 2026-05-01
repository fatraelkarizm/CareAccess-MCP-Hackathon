from typing import Annotated

from mcp.server.fastmcp import Context
from pydantic import Field

from fhir_client import FhirClient
from fhir_patient_summary import build_patient_summary
from fhir_utilities import get_fhir_context, get_patient_id_if_context_exists
from gemini_generation import generate_prior_auth_draft
from insurance_rules import generate_prior_auth_packet, get_coverage_decision
from mcp_utilities import create_text_response


def _format_yes_no(value: bool) -> str:
    return "yes" if value else "no"


def _decision(
    treatment: str,
    plan: str,
    diagnosis: str | None = None,
    clinical_context: str | None = None,
) -> dict:
    return get_coverage_decision(
        treatment=treatment,
        plan=plan,
        diagnosis=diagnosis,
        clinical_context=clinical_context,
    )


async def _patient_summary_from_fhir_context(ctx: Context | None) -> str | None:
    if not ctx:
        return None

    fhir_context = get_fhir_context(ctx)
    patient_id = get_patient_id_if_context_exists(ctx)
    if not fhir_context or not patient_id:
        return None

    fhir_client = FhirClient(base_url=fhir_context.url, token=fhir_context.token)
    patient = await fhir_client.read(f"Patient/{patient_id}")
    if not patient:
        return None

    condition_bundle = await fhir_client.search("Condition", {"patient": patient_id})
    conditions = [
        entry["resource"]
        for entry in (condition_bundle or {}).get("entry", [])
        if entry.get("resource")
    ]
    return build_patient_summary(patient, conditions)


async def _resolve_patient_summary(
    patient_summary: str | None,
    ctx: Context | None,
) -> tuple[str, str]:
    if patient_summary:
        return patient_summary, "manual input"

    fhir_summary = await _patient_summary_from_fhir_context(ctx)
    if fhir_summary:
        return fhir_summary, "SHARP/FHIR context"

    return "Synthetic/de-identified patient context unavailable", "fallback"


async def verify_coverage(
    treatment: Annotated[str, Field(description="Medication, procedure, imaging order, or lab to check")],
    plan: Annotated[str, Field(description="Synthetic insurance plan name")],
    diagnosis: Annotated[str | None, Field(description="Relevant diagnosis or condition")] = None,
    clinical_context: Annotated[str | None, Field(description="Short clinical context for the request")] = None,
) -> str:
    decision = _decision(treatment, plan, diagnosis, clinical_context)

    return create_text_response(
        "\n".join(
            [
                f"Treatment: {decision['treatment']}",
                f"Plan: {decision['plan']}",
                f"Coverage: {decision['coverage']}",
                f"Prior authorization required: {_format_yes_no(decision['prior_auth_required'])}",
                f"Estimated patient cost: {decision['estimated_patient_cost']}",
                f"Reason: {decision['reason']}",
            ]
        )
    )


async def check_prior_auth(
    treatment: Annotated[str, Field(description="Treatment to check for prior authorization")],
    plan: Annotated[str, Field(description="Synthetic insurance plan name")],
    diagnosis: Annotated[str | None, Field(description="Relevant diagnosis or condition")] = None,
    clinical_context: Annotated[str | None, Field(description="Short clinical context for the request")] = None,
) -> str:
    decision = _decision(treatment, plan, diagnosis, clinical_context)

    if decision["prior_auth_required"]:
        return create_text_response(
            f"Prior authorization is required for {decision['treatment']} under {decision['plan']}. "
            f"Reason: {decision['reason']}"
        )

    return create_text_response(
        f"Prior authorization is not required based on the current synthetic rule. Reason: {decision['reason']}"
    )


async def estimate_cost(
    treatment: Annotated[str, Field(description="Treatment to estimate patient cost for")],
    plan: Annotated[str, Field(description="Synthetic insurance plan name")],
) -> str:
    decision = _decision(treatment, plan)
    return create_text_response(
        f"Estimated patient cost for {decision['treatment']} under {decision['plan']}: "
        f"{decision['estimated_patient_cost']}."
    )


async def suggest_alternatives(
    treatment: Annotated[str, Field(description="Treatment to find covered alternatives for")],
    plan: Annotated[str, Field(description="Synthetic insurance plan name")],
) -> str:
    decision = _decision(treatment, plan)
    alternative = decision.get("covered_alternative")

    if not alternative:
        return create_text_response("No covered alternative is listed in the synthetic payer rule.")

    return create_text_response(
        f"Covered alternative for {decision['treatment']} under {decision['plan']}: {alternative}."
    )


async def generate_prior_auth(
    treatment: Annotated[str, Field(description="Treatment needing prior authorization")],
    plan: Annotated[str, Field(description="Synthetic insurance plan name")],
    diagnosis: Annotated[str, Field(description="Relevant diagnosis or condition")],
    patient_summary: Annotated[str | None, Field(description="Short synthetic or de-identified patient summary. Optional when SHARP/FHIR patient context is available.")] = None,
    clinical_context: Annotated[str | None, Field(description="Short clinical context for the request")] = None,
    ctx: Context = None,
) -> str:
    resolved_summary, _ = await _resolve_patient_summary(patient_summary, ctx)
    decision = _decision(treatment, plan, diagnosis, clinical_context)
    fallback_packet = generate_prior_auth_packet(patient_summary=resolved_summary, decision=decision)
    packet = await generate_prior_auth_draft(
        decision=decision,
        patient_summary=resolved_summary,
        fallback_text=fallback_packet,
    )
    return create_text_response(packet)


async def explain_benefits(
    treatment: Annotated[str, Field(description="Treatment to explain benefits for")],
    plan: Annotated[str, Field(description="Synthetic insurance plan name")],
) -> str:
    decision = _decision(treatment, plan)
    prior_auth_text = "requires prior authorization" if decision["prior_auth_required"] else "does not require prior authorization"

    return create_text_response(
        f"Your plan lists {decision['treatment']} as {decision['coverage']}. "
        f"It {prior_auth_text}. The estimated patient cost is "
        f"{decision['estimated_patient_cost']}. "
        "This is an estimate for decision support, not a payer guarantee."
    )


async def assess_treatment_access(
    treatment: Annotated[str, Field(description="Treatment to assess for access barriers")],
    plan: Annotated[str, Field(description="Synthetic insurance plan name")],
    diagnosis: Annotated[str, Field(description="Relevant diagnosis or condition")],
    patient_summary: Annotated[str | None, Field(description="Short synthetic or de-identified patient summary. Optional when SHARP/FHIR patient context is available.")] = None,
    clinical_context: Annotated[str | None, Field(description="Short clinical context for the request")] = None,
    ctx: Context = None,
) -> str:
    resolved_summary, context_source = await _resolve_patient_summary(patient_summary, ctx)
    decision = _decision(treatment, plan, diagnosis, clinical_context)
    fallback_packet = generate_prior_auth_packet(patient_summary=resolved_summary, decision=decision)
    packet = await generate_prior_auth_draft(
        decision=decision,
        patient_summary=resolved_summary,
        fallback_text=fallback_packet,
    )
    if decision["coverage"] == "not_covered":
        next_action = "Discuss covered alternatives, cash-pay implications, or appeal options with the patient."
    elif decision["prior_auth_required"]:
        next_action = "Review and submit the prior authorization packet."
    else:
        next_action = "Proceed with ordering workflow if clinically appropriate."

    brief = f"""# CareAccess MCP Treatment Access Brief

Treatment: {decision["treatment"]}
Plan: {decision["plan"]}
Patient: {resolved_summary}
Context source: {context_source}

## Access Decision
- Coverage: {decision["coverage"]}
- Prior authorization required: {_format_yes_no(decision["prior_auth_required"])}
- Estimated patient cost: {decision["estimated_patient_cost"]}
- Covered alternative: {decision.get("covered_alternative") or "No covered alternative listed."}

## Why
{decision["reason"]}

## Next best action
{next_action}

## Prior Authorization Packet Preview
{packet}

## Safety Note
This output is decision support based on synthetic rules. It is not medical advice or a payer guarantee.
"""

    return create_text_response(brief)
