# CareAccess MCP

> A Prompt Opinion MCP Superpower for checking insurance coverage, prior authorization, patient cost, and reviewable prior authorization drafts from healthcare context.

CareAccess MCP is a healthcare MCP server concept for the **Agents Assemble: Healthcare AI Endgame Challenge**. The goal is not to build a standalone healthcare app. The goal is to build a focused **MCP Superpower** that other agents in Prompt Opinion can invoke when a clinician needs insurance access guidance at the point of care.

## The Core Idea

Clinicians often choose treatments without real-time visibility into insurance
rules. That creates delayed care, surprise costs, extra administrative work, and
avoidable denials.

CareAccess MCP turns coverage checks into an agent-ready workflow:

1. Receive patient and encounter context from Prompt Opinion through SHARP/FHIR.
2. Match the requested treatment against synthetic payer rules.
3. Use Gemini to generate clear clinical and patient-facing explanations.
4. Return structured outputs that another agent or clinician can act on.

In short: **CareAccess MCP is an insurance coverage and prior authorization
superpower for healthcare agents.**

## What We Are Building

CareAccess MCP will expose a small set of MCP tools that answer practical insurance access questions:

- Is this medication, procedure, imaging order, or lab likely covered?
- Does it require prior authorization?
- What patient cost should the clinician expect?
- If prior authorization is needed, what reviewable packet can be drafted?
- Are there covered alternatives worth considering?

The first showcase flow is intentionally narrow:

> A clinician wants to prescribe Semaglutide for a synthetic Type 2 Diabetes patient. CareAccess MCP checks synthetic payer rules, identifies that prior authorization is required, estimates patient cost, suggests a covered alternative, and generates a draft prior authorization packet.

## What This Is Not

CareAccess MCP is not a diagnosis tool, medical advice engine, payer guarantee, or patient-facing chatbot. It is decision support for insurance access workflows, using synthetic or de-identified data for the hackathon demo.

## Implemented MVP MCP Tools

| Tool | Showcase Role |
| --- | --- |
| `assessTreatmentAccess` | Runs the full showcase flow in one call: coverage, prior authorization, cost, alternative, and packet preview. |
| `verifyCoverage` | Returns whether the requested treatment is likely covered under the synthetic plan. |
| `checkPriorAuth` | Explains whether prior authorization is required and what rule triggered it. |
| `estimateCost` | Estimates patient responsibility from synthetic benefit data. |
| `generatePriorAuth` | Produces a reviewable prior authorization packet draft. |
| `suggestAlternatives` | Suggests covered alternatives from the mock payer rules. |
| `explainBenefits` | Converts coverage details into patient-friendly language. |

## Showcase Output

```text
Treatment: Semaglutide
Patient context: Synthetic Type 2 Diabetes patient
Plan: Acme Silver PPO

Coverage: Covered with prior authorization
Prior authorization: Required
Reason: GLP-1 medications require diagnosis documentation and prior therapy trial
Estimated patient cost: $75/month
Covered alternative: Metformin ER, fully covered
Generated artifact: Draft prior authorization packet
```

The best single-call demo tool is `assessTreatmentAccess`. It returns a polished
Treatment Access Brief with the access decision, reason, next best action, and
prior authorization packet preview.

For the suggested 3-minute walkthrough, see `DEMO.md`.

## Architecture

```text
Prompt Opinion Agent
        |
        | MCP tool call + SHARP/FHIR context
        v
CareAccess MCP Server
        |
        +-- FHIR context utilities
        |     Reads patient and encounter context from SHARP/FHIR payloads
        |
        +-- Synthetic payer rules
        |     Models coverage, prior authorization, alternatives, and cost rules
        |
        +-- Gemini generation
        |     Drafts explanations and prior authorization text for human review
        |
        v
Structured MCP response
```

## Repository Structure

This repository is based on the Prompt Opinion community MCP starter. The project is now focused on the Python implementation, with the TypeScript starter kept as a reference while the first CareAccess tools are built.

```text
.
|-- python/              # Primary implementation target for CareAccess MCP
|-- typescript/          # Reference implementation from the starter
|-- scripts/             # Local Docker helper scripts
|-- DEMO.md              # 3-minute demo script and validation commands
|-- HACKATHON-TASK.md    # Hackathon notes and positioning
|-- UPSTREAM-README.md   # Original Prompt Opinion starter README
`-- README.md            # CareAccess MCP product showcase
```

The current product direction is to implement the showcase tools in `python/tools/` because the Python starter already includes MCP tool examples such as `patient_age_tool.py`, `patient_allergies_tool.py`, and `patient_id_tool.py`.

CareAccess-specific MVP tools live in `python/tools/coverage_tools.py`, with
synthetic payer rules in `python/insurance_rules.py`.

## Tech Direction

| Area | Direction |
| --- | --- |
| Track | Prompt Opinion Superpower, powered by MCP |
| Primary implementation | Python MCP server |
| Healthcare context | SHARP-on-MCP and FHIR R4 context |
| Demo data | Synthetic patient, plan, and payer rules |
| Generation | Gemini API for explanations and PA packet drafts |
| Runtime | Local MCP server, publishable to Prompt Opinion Marketplace |

## Environment Variables

```env
GEMINI_API_KEY=your_gemini_api_key_here
FHIR_BASE_URL=https://your-fhir-server.example
PORT=3000
```

For the hackathon demo, payer rules and coverage data can be synthetic and local. A production version would require real payer integrations, stronger audit controls, and validated cost estimation logic.

## Running the Python Starter

The Python server is the main CareAccess MCP implementation target. The root URL
is only a small health/info endpoint. The real MCP endpoint is `/mcp`, and it is
meant to be called by Prompt Opinion or an MCP client, not by opening it directly
in a normal browser tab.

### First-Time Setup

On Windows:

```powershell
cd python
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The server runs at:

```text
http://127.0.0.1:8000
```

Open that URL in a browser. You should see a small JSON response saying the
server is running.

### Run Again Later

After dependencies are installed once, you only need:

```powershell
cd python
venv\Scripts\activate
uvicorn main:app --reload
```

### Test the MCP Endpoint

Opening `/mcp` directly in a browser can return `406 Not Acceptable`. That is
normal because MCP expects a JSON-RPC request with MCP-compatible headers.

Use this PowerShell smoke test from the repository root:

```powershell
$headers = @{
  Accept = "application/json, text/event-stream"
  "Content-Type" = "application/json"
}

$body = @{
  jsonrpc = "2.0"
  id = 1
  method = "initialize"
  params = @{
    protocolVersion = "2025-06-18"
    capabilities = @{}
    clientInfo = @{
      name = "local-smoke-test"
      version = "0.1.0"
    }
  }
} | ConvertTo-Json -Depth 10

Invoke-WebRequest `
  -Uri http://127.0.0.1:8000/mcp `
  -Method Post `
  -Headers $headers `
  -Body $body `
  -UseBasicParsing
```

Expected result: HTTP `200` with MCP initialize data, including the
`ai.promptopinion/fhir-context` capability.

### Stop the Server

If uvicorn is running in your current terminal, press `Ctrl+C`.

If it was started in the background, find and stop it with:

```powershell
Get-CimInstance Win32_Process |
  Where-Object { $_.CommandLine -match "uvicorn" -and $_.CommandLine -match "main:app" } |
  ForEach-Object { Stop-Process -Id $_.ProcessId }
```

### Docker Option

With Docker from the repository root:

```powershell
docker compose -f docker-compose-local.yml up python --build
```

The Docker service maps the Python server to:

```text
http://127.0.0.1:55002
```

## Hackathon Positioning

**MCP Fit:** CareAccess MCP exposes reusable insurance access tools that any Prompt Opinion agent can invoke.

**FHIR/SHARP Fit:** The tools are designed to use healthcare context instead of custom one-off payloads.

**Gemini Usage:** Gemini helps convert rule results into readable explanations and draft prior authorization text.

**Impact:** The project targets a painful operational gap: treatment delays and administrative work caused by insurance friction.

**Feasibility:** The first demo can work with synthetic payer rules while still representing a realistic point-of-care workflow.
