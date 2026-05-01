from mcp.server.fastmcp import FastMCP
from tools.coverage_tools import (
    check_prior_auth,
    estimate_cost,
    explain_benefits,
    generate_prior_auth,
    suggest_alternatives,
    verify_coverage,
)
from tools.patient_age_tool import get_patient_age
from tools.patient_allergies_tool import get_patient_allergies
from tools.patient_id_tool import find_patient_id

mcp = FastMCP("CareAccess MCP", stateless_http=True, host="0.0.0.0")

_original_get_capabilities = mcp._mcp_server.get_capabilities

def _patched_get_capabilities(notification_options, experimental_capabilities):
    caps = _original_get_capabilities(notification_options, experimental_capabilities)
    caps.model_extra["extensions"] = {
        "ai.promptopinion/fhir-context": {
            "scopes": [
                {"name": "patient/Patient.rs", "required": True},
                {"name": "patient/Observation.rs"},
                {"name": "patient/MedicationStatement.rs"},
                {"name": "patient/Condition.rs"},
            ]
        }
    }
    return caps

mcp._mcp_server.get_capabilities = _patched_get_capabilities



mcp.tool(name="GetPatientAge", description="Gets the age of a patient.")(get_patient_age)
mcp.tool(name="GetPatientAllergies", description="Gets the known allergies of a patient.")(get_patient_allergies)
mcp.tool(name="FindPatientId", description="Finds a patient id given a first name and last name")(find_patient_id)
mcp.tool(name="verifyCoverage", description="Checks synthetic payer coverage for a requested treatment.")(verify_coverage)
mcp.tool(name="checkPriorAuth", description="Determines whether prior authorization is required.")(check_prior_auth)
mcp.tool(name="estimateCost", description="Estimates patient responsibility from synthetic benefit rules.")(estimate_cost)
mcp.tool(name="generatePriorAuth", description="Generates a reviewable prior authorization draft.")(generate_prior_auth)
mcp.tool(name="suggestAlternatives", description="Suggests covered alternatives from synthetic payer rules.")(suggest_alternatives)
mcp.tool(name="explainBenefits", description="Explains coverage details in patient-friendly language.")(explain_benefits)
