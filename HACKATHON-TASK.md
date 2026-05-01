# Agents Assemble: The Healthcare AI Endgame Challenge

Build interoperable healthcare agents at the intersection of **MCP**, **A2A**,
and **FHIR**.

## Challenge Summary

Prompt Opinion describes this hackathon as a "Last Mile" challenge: turning raw
AI capability into concrete healthcare deliverables that can be invoked inside a
clinician workflow.

Participants must build and demonstrate a healthcare MCP or agent solution that integrates
with the Prompt Opinion platform.

## Submission Paths

### Option 1: Build a Superpower (Powered by MCP)

Create an MCP server that exposes a focused set of healthcare tools. These tools
can be discovered and invoked by agents inside the Prompt Opinion ecosystem.

This is the best fit for **CareAccess MCP** because the project exposes reusable
insurance access tools such as coverage verification, prior authorization checks,
cost estimation, and prior authorization packet generation.

### Option 2: Build an Agent (Powered by A2A)

Configure an intelligent agent that handles a broader healthcare workflow. Prompt
Opinion supports A2A behavior inside the platform, so builders can focus on the
use case instead of implementing the protocol from scratch.

## Required Workflow

1. Register for the hackathon and create a Prompt Opinion account.
2. Build an MCP server or A2A agent using your own infrastructure.
3. Integrate SHARP context handling for healthcare context such as patient IDs
   and FHIR tokens.
4. Use FHIR data when possible. It is highly recommended, even if not strictly
   required.
5. Publish the project to the Prompt Opinion Marketplace.
6. Submit a demo video under 3 minutes showing the project working inside Prompt
   Opinion.

## Why Prompt Opinion Matters

- **Standards built in:** MCP and A2A support reduce custom integration work.
- **SHARP context propagation:** EHR session context can flow into tools and
  agents through healthcare-aware context.
- **No vendor lock-in:** Open standards make tools easier to reuse or replace.
- **Agent composition:** Specialist agents and tools can be combined into larger
  healthcare workflows.

## CareAccess MCP Fit

CareAccess MCP should be positioned as an **MCP Superpower**:

- It receives patient and clinical context through SHARP/FHIR.
- It checks synthetic payer rules for coverage, prior authorization, alternatives,
  and estimated patient cost.
- It uses Gemini to generate reviewable explanations and prior authorization
  drafts.
- It returns structured outputs that clinicians or other agents can act on.

## Important Dates

- Submission period: Monday, March 4, 2026 to Monday, May 11, 2026.
- Winners announced: On or around Wednesday, May 27, 2026.

## Reference

Getting started video: https://youtu.be/Qvs_QK4meHc
