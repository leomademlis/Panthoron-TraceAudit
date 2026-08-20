# 🏭 Panthoron TraceAudit Agent

An autonomous, Agentic AI workflow designed to revolutionize Food Safety and Quality Assurance for the industrial food sector. Built for the Google AI Hackathon on Devpost.

## 🚀 Overview
When a contaminated raw material is detected on the factory floor, Panthoron acts as a digital Senior Quality Manager. Powered by the Google **Gemini 3.5 Flash** model, the Agent does not just converse; it autonomously uses custom Python tools (Function Calling) to solve complex traceability problems.

## 🛠️ Key Features
* **Agentic Function Calling:** Uses custom Python tools to perform rigid, deterministic tasks.
* **Dynamic Time Calculations:** Mathematically calculates physical factory constraints (conveyor belt times + freezing tunnel duration) to pinpoint precise contamination windows.
* **ERP & Logistics Mock Integration:** Simulates retrieving carton LPNs from production databases and scanning Google Drive PDFs to track shipped pallets to their final customers.
* **Automated URGENT RECALL REPORTING:** Outputs a perfectly structured, English-language quarantine report in under 10 seconds, ready for management and IFS/BRC audits.

## 💻 Tech Stack
* Python
* `google-genai` SDK
* **Google Gemini 3.5 Flash**
* Google Colab (PoC Environment)

## ⚠️ Note for Judges
This repository contains the Proof of Concept (PoC) code demonstrating the Agentic Workflow. For the hackathon demo, the Google Workspace (Drive/Sheets) integrations and ERP databases are mocked via Python functions to ensure a stable, frictionless presentation of the AI's autonomous reasoning and tool-calling capabilities.

---

## ⚙️ How to Run (Spin-up Instructions)

Follow these step-by-step instructions to reproduce the Agent's workflow from scratch. 
*Note: Because this is a Proof of Concept (PoC) built for the hackathon, the Google Workspace APIs (Sheets & Drive) are mocked via Python functions. You do not need to configure OAuth 2.0 or Service Accounts to run this demo!*

### Step 1: Open the Environment
We recommend running this project in **Google Colab** for a frictionless experience.
1. Download the `Panthoron_TraceAudit_Agent(2).ipynb` file from this repository.
2. Go to [Google Colab](https://colab.research.google.com/) and upload the notebook.

### Step 2: Install Dependencies
The project uses the latest Google GenAI SDK. Run the very first cell in the notebook to install it:
```python
!pip install -q -U google-genai

Step 3: Insert Your API Key

To run the Gemini 3.5 Flash model, you need an API key from Google AI Studio / Cloud Console.

    Locate the main code block in the notebook.

    Find this line: GOOGLE_API_KEY = "YOUR_API_KEY_HERE"

    Replace "YOUR_API_KEY_HERE" with your actual API key (keep the quotation marks).

Step 4: Execute the Agent

    Run the code block.

    The script will initialize the Panthoron TraceAudit Agent persona and pass a simple crisis email containing ONLY the contaminated Lot Number.

    Scroll down to see the Agent autonomously reasoning and invoking its four tools sequentially (fetch_lot_production_data, calculate_quarantine_window, search_boxes_in_google_sheets, scan_google_drive_for_shipping) to uncover the full traceability path without human intervention.

Step 5: Expected Output

Within 5-10 seconds, the model will output a fully structured OFFICIAL URGENT RECALL REPORT in the console, confirming the pallet's LPN, the blocked status, and the shipping details.
