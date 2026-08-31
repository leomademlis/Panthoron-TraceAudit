🏭 Panthoron TraceAudit AgentA B2B Gemini-powered AI agent that transforms complex food manufacturing data (ERP, production logic, and logistics PDFs) into instant, autonomous product recalls.
📌 The Problem (Born from 27 Years on the Plant Floor)When a contamination is suspected, human teams spend hours rebuilding a trace out of folders and spreadsheets, while product sits on hold and nobody can tell the retailer anything. Tracing a contaminated raw material (e.g., E. coli) through complex ERP systems, dynamic freezing tunnels, and scattered shipping documents takes hours of manual panic. Delays in food safety don't just cost money; they cost lives.
🚀 The SolutionPanthoron TraceAudit is a fully autonomous digital Senior Quality Manager. Triggered by a single urgent email, the AI agent takes over with no prompting, no chat, and no human in the loop. It executes a sophisticated multi-tool chain:
ERP Query: Extracts the contaminated lot number and finds the exact line drop time.
Production Maths: Calculates physical factory constraints (conveyor + freezing tunnel times) to pinpoint the exact exit time.
Google Sheets (Inventory): Cross-references the database to isolate the specific Master Pallet (LPN) and mark it blocked.
Google Drive (Logistics): Scans shipping PDFs to intercept moving trucks, extracting license plates, documents, and customer data.
Within seconds, it synthesizes this data into an actionable Draft Recall Report. The agent does not invent data; every figure comes from a tool call and can be traced back to its source.
🛠️ Engineering & Tech StackAI 
Brain: Google Gemini 3.5 Flash (via google-genai SDK).
Architecture: Agentic Function Calling. Each tool is independently callable and the chain is stateless between requests. If a tool fails, the agent flags the gap rather than guessing or hallucinating.
Infrastructure: Runs as a live API on Google Cloud Run (europe-west1).
Language: Python 3.
⚡ Try it Live (For Judges)Panthoron is deployed live on Google Cloud Run. You can trigger the Agent and see it autonomously resolve the crisis right from your terminal.Open your terminal (Mac/Linux) or Google Cloud Shell and paste the following command:

curl -s -X POST https://panthoron-agent-778793548190.europe-west1.run.app/run-audit \
-H "Content-Type: application/json" \
-d '{
  "crisis_email": "URGENT NOTIFICATION FROM SUPPLIER: We just detected severe Escherichia coli (E. coli) contamination in Raw Material Lot: 260707AH. Please investigate immediately.",
  "api_key": "YOUR_GEMINI_API_KEY"
}' | jq -r '.recall_report'

(Note: Please allow a few seconds for the Agent to execute its function chain and stream back the formatted Draft Recall Report.)Disclaimer: All customer names, addresses, and vehicle plates generated or used in this demo are 100% synthetic test data and do not correspond to any real ERP records.
