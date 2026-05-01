# CareAccess MCP Demo Script

This is a 3-minute demo outline for the Prompt Opinion Agents Assemble Hackathon.

## Demo Goal

Show that CareAccess MCP is not a generic chatbot. It is a reusable MCP
Superpower that gives healthcare agents a concrete insurance access workflow:
coverage, prior authorization, cost, alternatives, and a reviewable packet draft.

## 30-Second Pitch

CareAccess MCP helps healthcare agents remove insurance friction at the point of
care. When a clinician wants to order a treatment, the agent can call this MCP
server to check whether the treatment is covered, whether prior authorization is
needed, what the patient may pay, what alternatives are covered, and what packet
should be prepared for human review.

The demo uses synthetic payer rules and synthetic patient context. It is decision
support, not medical advice or a payer guarantee.

## Recommended Demo Flow

1. Open the local server health endpoint:

   ```text
   http://127.0.0.1:8000/
   ```

   Show that the CareAccess MCP server is running.

2. Explain the hero tool:

   ```text
   assessTreatmentAccess
   ```

   This single MCP tool runs the full showcase workflow.

3. Run the Semaglutide scenario:

   ```powershell
   $headers = @{
     Accept = "application/json, text/event-stream"
     "Content-Type" = "application/json"
   }

   $body = @{
     jsonrpc = "2.0"
     id = 1
     method = "tools/call"
     params = @{
       name = "assessTreatmentAccess"
       arguments = @{
         treatment = "Semaglutide"
         plan = "Acme Silver PPO"
         diagnosis = "Type 2 Diabetes"
         patient_summary = "Synthetic patient with Type 2 Diabetes"
         clinical_context = "A1C above goal after metformin trial"
       }
     }
   } | ConvertTo-Json -Depth 10

   $response = Invoke-WebRequest `
     -Uri http://127.0.0.1:8000/mcp `
     -Method Post `
     -Headers $headers `
     -Body $body `
     -UseBasicParsing

   $json = $response.Content -replace "^event: message\s*data: ", "" | ConvertFrom-Json
   $json.result.content[0].text
   ```

4. Point out the result:

   - Coverage: covered with prior authorization
   - Estimated patient cost: $75/month
   - Covered alternative: Metformin ER
   - Next best action: review and submit prior authorization packet
   - Human review required before submission

5. Close with marketplace value:

   CareAccess MCP can be invoked by any Prompt Opinion agent that needs insurance
   access intelligence. The MCP interface makes the capability reusable instead
   of locking it inside one app.

## Extra Scenarios

Use these if the demo needs more variety.

### Imaging Prior Authorization

```text
Treatment: Lumbar Spine MRI
Plan: Acme Silver PPO
Diagnosis: Low back pain with radiculopathy
Clinical context: Persistent symptoms after conservative therapy
Expected: Covered with prior authorization, $150 imaging copay
```

### Covered Lab

```text
Treatment: HbA1c Lab
Plan: Acme Silver PPO
Diagnosis: Type 2 Diabetes
Clinical context: Routine diabetes monitoring
Expected: Covered, no prior authorization, $0 preventive lab benefit
```

### Not Covered Medication

```text
Treatment: Wegovy
Plan: Acme Silver PPO
Diagnosis: Weight management
Clinical context: No diabetes diagnosis documented
Expected: Not covered, full retail cost, suggest nutrition counseling benefit
```

## Judge-Friendly Talking Points

- MCP fit: tools are discoverable and callable through a standard protocol.
- Healthcare fit: the server declares SHARP/FHIR context capability.
- Impact: targets treatment delays caused by coverage uncertainty and prior auth.
- Safety: synthetic data, human review, no payer guarantee, no medical advice.
- Feasibility: works locally today and can be expanded with real payer/FHIR data.

## What To Avoid Saying

- Do not claim real payer accuracy.
- Do not claim the prior authorization packet is submission-ready without review.
- Do not present this as diagnosis or treatment recommendation software.
- Do not frame it as a patient chatbot.
