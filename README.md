# CareAccess MCP

> An MCP-powered insurance access copilot for point-of-care healthcare decisions.

CareAccess MCP helps clinicians quickly understand whether a medication, procedure,
lab, or imaging order is likely covered by a patient's insurance plan, whether
prior authorization is needed, what alternatives may be covered, and what the
patient may need to pay.

"CareAccess MCP is a Superpower server that helps healthcare agents remove insurance friction at the point of care by checking coverage, prior authorization, patient cost, and generating reviewable PA packets from FHIR/SHARP context."

Built for the Prompt Opinion Agents Assemble Hackathon, this project focuses on
the **Superpower (MCP)** track: a reusable MCP server that other agents can invoke
inside Prompt Opinion using SHARP/FHIR healthcare context.

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

## MVP Scope

For the hackathon demo, the most important flow is:

- Check if a requested treatment is covered.
- Detect whether prior authorization is required.
- Estimate patient responsibility from synthetic benefit data.
- Generate a draft prior authorization packet when needed.

Nice-to-have features:

- Suggest covered alternatives.
- Explain benefits in patient-friendly language.

## MCP Tools

| Tool | Purpose |
| --- | --- |
| `verifyCoverage` | Checks whether a medication, procedure, imaging order, or lab is likely covered. |
| `checkPriorAuth` | Determines whether prior authorization is required and why. |
| `estimateCost` | Estimates deductible, copay, coinsurance, and patient responsibility. |
| `generatePriorAuth` | Drafts a prior authorization packet with clinical justification. |
| `suggestAlternatives` | Recommends clinically relevant covered alternatives. |
| `explainBenefits` | Converts coverage details into patient-friendly language. |

## Example Demo Flow

**Input**

```text
Patient: Synthetic patient with Type 2 Diabetes
Medication: Semaglutide
Plan: Acme Silver PPO
Clinical context: A1C above goal after metformin trial
```

**Output**

```text
Coverage: Covered with prior authorization
Prior authorization: Required
Reason: GLP-1 medications require documented diagnosis and previous therapy trial
Estimated patient cost: $75/month
Covered alternative: Metformin ER, fully covered
Generated artifact: Draft prior authorization packet
```

## Architecture

```text
Prompt Opinion UI / Agent
        |
        | MCP tool invocation with SHARP context
        v
CareAccess MCP Server
        |
        +-- FHIR service
        |     Reads patient, medication, condition, and encounter context
        |
        +-- Insurance rules service
        |     Looks up synthetic payer coverage and prior authorization rules
        |
        +-- Gemini service
        |     Generates explanations and prior authorization drafts
        |
        v
Structured MCP tool response
```

## Tech Stack

| Area | Choice |
| --- | --- |
| Backend | Node.js, Express.js, TypeScript |
| MCP | Model Context Protocol server tools |
| Generation | Gemini API |
| Healthcare context | FHIR R4, SHARP context propagation |
| Data | Synthetic payer rules and mock coverage data |
| Database | PostgreSQL |
| Cache | Redis optional |
| Testing | Vitest |
| Deployment | Docker, Railway, Render, or Fly.io |

## Suggested Folder Structure

```text
careaccess-mcp/
|-- src/
|   |-- server.ts
|   |-- mcp/
|   |   |-- tools/
|   |   |-- schemas/
|   |   `-- registry.ts
|   |-- services/
|   |   |-- gemini.ts
|   |   |-- fhir.ts
|   |   `-- insurance.ts
|   |-- data/
|   |   `-- synthetic-payer-rules.ts
|   |-- utils/
|   `-- types/
|-- tests/
|-- docker-compose.yml
|-- Dockerfile
|-- package.json
`-- README.md
```

## Getting Started

### Prerequisites

- Node.js 20+
- PostgreSQL
- Gemini API key
- Access to Prompt Opinion for MCP registration

### Environment Variables

```env
GEMINI_API_KEY=your_gemini_api_key_here
FHIR_BASE_URL=https://your-fhir-server.example
DATABASE_URL=postgresql://localhost:5432/careaccess
PORT=3000
```

### Run Locally

```bash
npm install
npm run dev
```

## Prompt Opinion Integration

1. Publish CareAccess MCP as an MCP server.
2. Register the MCP tools in the Prompt Opinion Marketplace.
3. Enable SHARP context propagation for patient and FHIR access context.
4. Test invocation from a Prompt Opinion agent or workspace.
5. Record a demo video under 3 minutes.

## Compliance Notes

- Use synthetic or de-identified data only.
- Do not require production PHI for the hackathon demo.
- Treat cost and coverage outputs as decision support estimates, not payer guarantees.
- Keep generated prior authorization text reviewable by a clinician or administrator.

## Hackathon Alignment

**Gemini Usage:** Uses Gemini to summarize rules, explain benefits, and draft prior
authorization packets.

**MCP Fit:** Exposes coverage intelligence as reusable MCP tools that other
agents can invoke.

**FHIR/SHARP Fit:** Uses patient and clinical context from healthcare standards
instead of custom one-off payloads.

**Impact:** Reduces treatment delays, administrative burden, and preventable
coverage friction.

**Feasibility:** Demoable with synthetic payer rules and mock FHIR data while
still matching a real healthcare workflow.
