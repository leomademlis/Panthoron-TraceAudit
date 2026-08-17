# 🏭 Panthoron TraceAudit Agent

An autonomous, Agentic AI workflow designed to revolutionize Food Safety and Quality Assurance for the industrial food sector. Built for the Google AI Hackathon on Devpost.

## 🚀 Overview
When a contaminated raw material is detected on the factory floor, Panthoron acts as a digital Senior Quality Manager. Powered by the newly released **Google Gemini 2.5 Flash**, the Agent does not just converse; it autonomously uses custom Python tools (Function Calling) to solve complex traceability problems.

## 🛠️ Key Features
* **Agentic Function Calling:** Uses custom Python tools to perform rigid, deterministic tasks.
* **Dynamic Time Calculations:** Mathematically calculates physical factory constraints (conveyor belt times + freezing tunnel duration) to pinpoint precise contamination windows.
* **ERP & Logistics Mock Integration:** Simulates retrieving carton LPNs from production databases and scanning Google Drive PDFs to track shipped pallets to their final customers.
* **Automated URGENT RECALL REPORTING:** Outputs a perfectly structured, English-language quarantine report in under 10 seconds, ready for management and IFS/BRC audits.

## 💻 Tech Stack
* Python
* `google-genai` SDK
* Gemini 2.5 Flash
* Google Colab (PoC Environment)

## ⚠️ Note for Judges
This repository contains the Proof of Concept (PoC) code demonstrating the Agentic Workflow. For the hackathon demo, the Google Workspace (Drive/Sheets) integrations and ERP databases are mocked via Python functions to ensure a stable, frictionless presentation of the AI's autonomous reasoning and tool-calling capabilities.
