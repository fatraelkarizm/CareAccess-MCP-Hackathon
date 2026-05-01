from copy import deepcopy


SYNTHETIC_PAYER_RULES = {
    "acme silver ppo": {
        "semaglutide": {
            "treatment": "Semaglutide",
            "coverage": "covered_with_prior_auth",
            "prior_auth_required": True,
            "estimated_patient_cost": "$75/month",
            "covered_alternative": "Metformin ER",
            "reason": (
                "GLP-1 medications require documented Type 2 Diabetes diagnosis, "
                "recent A1C, and prior therapy trial."
            ),
            "documentation_required": [
                "Type 2 Diabetes diagnosis",
                "Recent A1C result",
                "Previous metformin trial or contraindication",
                "Current medication list",
            ],
        }
    }
}


def get_coverage_decision(
    treatment: str,
    plan: str,
    diagnosis: str | None = None,
    clinical_context: str | None = None,
) -> dict:
    plan_rules = SYNTHETIC_PAYER_RULES.get(plan.strip().lower(), {})
    rule = plan_rules.get(treatment.strip().lower())

    if not rule:
        return {
            "treatment": treatment,
            "plan": plan,
            "diagnosis": diagnosis,
            "clinical_context": clinical_context,
            "coverage": "unknown",
            "prior_auth_required": False,
            "estimated_patient_cost": "unknown",
            "covered_alternative": None,
            "reason": "No synthetic payer rule was found for this treatment and plan.",
            "documentation_required": [],
        }

    decision = deepcopy(rule)
    decision["plan"] = plan
    decision["diagnosis"] = diagnosis
    decision["clinical_context"] = clinical_context
    return decision


def generate_prior_auth_packet(patient_summary: str, decision: dict) -> str:
    documentation = decision.get("documentation_required") or []
    documentation_lines = "\n".join(f"- {item}" for item in documentation)

    return f"""Prior Authorization Draft

Treatment: {decision.get("treatment")}
Plan: {decision.get("plan")}
Patient Summary: {patient_summary}

Clinical Rationale:
{decision.get("reason")}

Required Documentation:
{documentation_lines or "- No additional documentation listed in synthetic rule."}

Estimated Patient Cost:
{decision.get("estimated_patient_cost")}

Covered Alternative:
{decision.get("covered_alternative") or "No covered alternative listed."}

Human Review Required:
This draft is decision support only. A clinician or administrator must review it before submission.
"""
