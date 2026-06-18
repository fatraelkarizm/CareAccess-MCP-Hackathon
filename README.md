# PriorMCP: Healthcare Insurance Access Agent 🚀

> A Model Context Protocol (MCP) Superpower for real-time insurance coverage verification, prior authorization, cost estimation, and packet generation.

[![Tech Stack: Python](https://img.shields.io/badge/Tech-Python-blue.svg)](https://www.python.org/)
[![Protocol: MCP](https://img.shields.io/badge/Protocol-MCP-orange.svg)](https://github.com/prompt-opinion/mcp)
[![AI: Gemini](https://img.shields.io/badge/AI-Google_Gemini-blueviolet.svg)](https://deepmind.google/technologies/gemini/)
[![Standard: FHIR](https://img.shields.io/badge/Standard-FHIR_R4-red.svg)](https://hl7.org/fhir/)

## 📖 1. Overview
**PriorMCP** is an interoperable healthcare AI service built as an **MCP Server** for the Prompt Opinion "Agents Assemble" hackathon. Rather than operating as a standalone chatbot, PriorMCP acts as a backend *Superpower* that other healthcare agents can invoke. It provides immediate point-of-care insurance intelligence by analyzing synthetic payer rules, estimating costs, and auto-drafting prior authorization packets using clinical context.

## ⚠️ 2. Problem Statement
In the healthcare industry, clinicians frequently prescribe treatments or order procedures without real-time visibility into the patient's insurance coverage rules. This lack of transparency causes:
* **Delayed Care:** Patients wait weeks while administrative staff process prior authorizations manually.
* **Surprise Costs:** Patients face unexpected out-of-pocket expenses for uncovered treatments.
* **Administrative Burden:** Clinics spend countless hours deciphering complex payer rules and handling avoidable claim denials.

## 💡 3. Solution
PriorMCP solves this friction by bringing insurance intelligence directly to the point of care via the Model Context Protocol. By exposing a suite of specialized tools to healthcare AI agents, it seamlessly:
1. **Ingests Context:** Uses SHARP/FHIR extensions to securely read patient IDs and encounter context from the EHR.
2. **Evaluates Rules:** Matches the requested treatment against synthetic, deterministic payer policies.
3. **Generates Intelligence:** Employs **Google Gemini** to instantly draft reviewable, clinical explanations and prior authorization packets.
4. **Delivers Actionable Outputs:** Returns a structured summary—including coverage status, cost, and covered alternatives—that clinicians or other agents can immediately act upon.

## ⚙️ 4. Key Features & Tech Stack

### Key Features
* **`assessTreatmentAccess`:** A single-call tool that runs the complete end-to-end workflow (coverage, prior auth, cost, alternative, and packet preview).
* **Coverage Verification (`verifyCoverage`):** Real-time checks against mocked payer rules.
* **Prior Authorization Engine (`checkPriorAuth` & `generatePriorAuth`):** Evaluates requirements and auto-drafts submission-ready PA packets for human review.
* **Cost Estimation (`estimateCost`):** Calculates expected patient responsibility.
* **EHR Interoperability:** Implements Prompt Opinion's FHIR context extension (`ai.promptopinion/fhir-context`) to support `x-fhir-server-url` and `x-patient-id`.

### Tech Stack
* **Language & Framework:** Python 3.10+, FastAPI, Uvicorn
* **Protocol:** Model Context Protocol (via `mcp` / `fastmcp`)
* **Generative AI:** Google Gemini 2.0 Flash (`google-genai` integration)
* **Healthcare Standards:** FHIR R4 (Synthetic EHR mockups)
* **Deployment & Infrastructure:** Docker & Local Virtual Environment

## 🚀 5. Getting Started

Follow these steps to run PriorMCP locally.

### Prerequisites
* Python 3.10 or higher
* [Docker](https://www.docker.com/) (Optional, for containerized run)
* A Google Gemini API Key (`GEMINI_API_KEY`)

### Installation & Local Run (Virtual Environment)
1. **Clone the repository and navigate to the project directory:**
   ```bash
   git clone <your-repo-url>
   cd healthcare-mcp/python
   ```
2. **Set up the virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```
3. **Configure Environment Variables:**
   Create a `.env` file in the `python/` directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_MODEL=gemini-2.0-flash
   PORT=8000
   ```
4. **Start the MCP Server:**
   ```bash
   uvicorn main:app --reload
   ```
   *The server health endpoint will be running at `http://127.0.0.1:8000`.*

### Installation via Docker
To run the server in a Docker container, execute from the repository root:
```bash
docker compose -f docker-compose-local.yml up python --build
```

---
*Disclaimer: PriorMCP uses synthetic data and rules for demonstration purposes. It is an administrative decision-support tool, not a provider of medical advice or an official payer guarantee.*
