def _human_name(patient: dict) -> str:
    names = patient.get("name") or []
    if not names:
        return "name unavailable"

    primary = names[0]
    given = " ".join(primary.get("given") or [])
    family = primary.get("family") or ""
    full_name = " ".join(part for part in [given, family] if part).strip()
    return full_name or primary.get("text") or "name unavailable"


def _condition_name(condition: dict) -> str | None:
    code = condition.get("code") or {}
    if code.get("text"):
        return code["text"]

    codings = code.get("coding") or []
    if codings:
        return codings[0].get("display")

    return None


def build_patient_summary(patient: dict, conditions: list[dict] | None = None) -> str:
    patient_id = patient.get("id") or "unknown"
    name = _human_name(patient)
    gender = patient.get("gender") or "gender unavailable"
    birth_date = patient.get("birthDate") or "birth date unavailable"

    condition_names = []
    for condition in conditions or []:
        condition_name = _condition_name(condition)
        if condition_name:
            condition_names.append(condition_name)
    condition_text = ", ".join(condition_names) if condition_names else "none available"

    return (
        f"FHIR Patient/{patient_id}: {name}, {gender}, born {birth_date}. "
        f"Conditions: {condition_text}."
    )
