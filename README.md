# 🏭 Panthoron TraceAudit Agent

> A B2B Gemini-powered AI agent that transforms complex food manufacturing data (ERP, production logic, and logistics PDFs) into instant, autonomous product recalls.

## 📌 The Problem
When a food contamination crisis hits, every second counts. Tracing a contaminated raw material (e.g., *E. coli*) through complex ERP systems, dynamic freezing tunnels, and scattered shipping documents takes hours of manual panic. Delays in food safety don't just cost money; they cost lives.

## 🚀 The Solution
Panthoron TraceAudit is a fully autonomous digital Senior Quality Manager deployed on Google Cloud Run. Triggered by a single urgent email, the AI agent executes a sophisticated multi-tool chain:
* **ERP Query:** Extracts the contaminated lot number and finds the exact line drop time.
* **Mathematical Logic:** Calculates physical factory constraints (conveyor + freezing tunnel times) to pinpoint the exact exit time.
* **Inventory Tracking:** Cross-references the mock database to isolate the specific Master Pallet (LPN).
* **Logistics Analysis:** Scans mocked shipping PDFs to intercept moving trucks, extracting license plates and customer data.

Within 20 seconds, it synthesizes this data into an official, actionable Urgent Recall Report.

## 🛠️ Tech Stack
* **AI Brain:** Google Gemini 3.5 Flash (via `google-genai` SDK)
* **Architecture:** Agentic Function Calling (Multi-tool reasoning)
* **Infrastructure:** Google Cloud Run (Stateless microservice)
* **Language:** Python 3

## ⚡ Try it Live (For Judges)
Panthoron is deployed live on Google Cloud Run. You can trigger the Agent and see it autonomously resolve the crisis right from your terminal.

Open your terminal (Mac/Linux) or Google Cloud Shell and paste the following command:

```bash
curl -s -X POST [https://panthoron-agent-778793548190.europe-west1.run.app/run-audit](https://panthoron-agent-778793548190.europe-west1.run.app/run-audit) \
-H "Content-Type: application/json" \
-d '{
  "crisis_email": "URGENT NOTIFICATION FROM SUPPLIER: We just detected severe Escherichia coli (E. coli) contamination in Raw Material Lot: 260707AH. Please investigate immediately.",
  "api_key": "YOUR_GEMINI_API_KEY"
}' | jq -r '.recall_report'

(Note: Please allow 15-30 seconds for the Agent to execute its function chain and stream back the formatted Official Recall Report.)
