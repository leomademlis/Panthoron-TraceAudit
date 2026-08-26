import os
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types

# Αρχικοποίηση της Web Εφαρμογής
app = FastAPI(title="Panthoron TraceAudit API", description="Autonomous Agent for Food Traceability")

# Μορφή δεδομένων που δέχεται το API (το αίτημα)
class TraceRequest(BaseModel):
    crisis_email: str
    api_key: str

# ------------------------------------------------------------------------------
# 1. THE 4 TOOLS OF THE AGENT
# ------------------------------------------------------------------------------
def fetch_lot_production_data(lot_number: str) -> str:
    """Queries the ERP database to find exactly where and when a contaminated raw material lot was used."""
    return "Lot found. Used on Production Line 1. Drop time: 03:33:53. Final product code: 09118. Line 1 constraints: 5-minute conveyor time, 35-minute freezing tunnel time."

def calculate_quarantine_window(drop_time: str, conveyor_mins: int, tunnel_mins: int) -> str:
    """Mathematically calculates the exact time the contaminated product exits the freezing tunnel."""
    time_format = "%H:%M:%S"
    drop_dt = datetime.strptime(drop_time, time_format)
    total_mins = conveyor_mins + tunnel_mins
    exit_dt = drop_dt + timedelta(minutes=total_mins)
    exit_time_str = exit_dt.strftime(time_format)
    return f"The contaminated product exited the freezing tunnel starting exactly at {exit_time_str}."

def search_boxes_in_google_sheets(exit_window_start: str) -> str:
    """Queries the industrial ERP database to identify the affected Master Pallet LPN based on the exit time."""
    return "Found matching production batch. Affected Pallet ID is LPN-260724-7153. Pallet status successfully changed to 'BLOCKED' in the database."

def scan_google_drive_for_shipping(pallet_lpn: str) -> str:
    """Simulates scanning Google Drive PDFs to check if the blocked pallet has already been shipped."""
    return "CRITICAL: Pallet LPN-260724-7153 has been shipped. Document matched: '24072026FINAL.pdf'. Customer: M. OGKOUNSOTO M.IKE, Address: Tsimiski 82, Thessaloniki. Loading Vehicle: NBX7849."

# ------------------------------------------------------------------------------
# 2. THE ENDPOINT OF CLOUD RUN
# ------------------------------------------------------------------------------
@app.post("/run-audit")
def run_audit(request: TraceRequest):
    if not request.api_key:
        raise HTTPException(status_code=400, detail="API Key is missing.")

    # Αρχικοποίηση του Client με το κλειδί που θα έρθει από το αίτημα
    client = genai.Client(api_key=request.api_key)

    current_date = datetime.now().strftime("%B %d, %Y")
    
    agent_persona = f"""
    You are the 'Panthoron TraceAudit Agent', an autonomous Senior Quality Manager for an industrial food factory.
    Your primary directive is to handle food safety crises swiftly and accurately.
    You strictly follow IFS, BRC, and ISO food safety standards.

    When you receive a crisis alert containing a contaminated Lot Number:
    1. NEVER guess or hallucinate data.
    2. ALWAYS use your tools sequentially to investigate:
       - First, find when and where the lot was used.
       - Second, calculate the physical time constraints (freezing tunnel exit time).
       - Third, find the affected Pallet LPN.
       - Fourth, check logistics to see if it has been shipped.
    3. Synthesize all data into a highly professional 'OFFICIAL URGENT RECALL REPORT'.
    4. Structure the report beautifully using Markdown (bold headers, bullet points).
    5. CRITICAL RULE: The exact current date is {current_date}. You MUST use this exact date in the DATE field of your official report.
    """

    try:
        # Δημιουργία Chat Session με τα 4 εργαλεία
        chat = client.chats.create(
            model="gemini-3.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=agent_persona,
                tools=[fetch_lot_production_data, calculate_quarantine_window, search_boxes_in_google_sheets, scan_google_drive_for_shipping],
                temperature=0.1,
            )
        )

        # Ο Agent διαβάζει το email και ξεκινάει την αλυσίδα των Functions
        response = chat.send_message(request.crisis_email)

        return {
            "status": "success",
            "agent_type": "Taskmaster",
            "recall_report": response.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
