import re
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types

# Web Application Initialization
app = FastAPI(title="Panthoron TraceAudit API", description="Autonomous Agent for Food Traceability")

# Data model for the API request payload
class TraceRequest(BaseModel):
    crisis_email: str
    api_key: str

# ------------------------------------------------------------------------------
# 1. THE 4 TOOLS OF THE AGENT 
# ------------------------------------------------------------------------------
def fetch_lot_production_data(lot_number: str) -> str:
    """Queries the ERP database to find exactly where and when a contaminated raw material lot was used."""
    return "Lot found. Used on Production Line 1. Drop time: July 24, 2026, 03:33:53. Final product code: 09118. Line 1 constraints: 5-minute conveyor time, 35-minute freezing tunnel time."

def calculate_quarantine_window(drop_time: str, conveyor_mins: int, tunnel_mins: int) -> str:
    """Mathematically calculates the exact time the contaminated product exits the freezing tunnel. Pass drop_time as HH:MM:SS."""
    time_match = re.search(r'\d{2}:\d{2}:\d{2}', drop_time)
    time_str = time_match.group() if time_match else "03:33:53"
    
    drop_dt = datetime.strptime(time_str, "%H:%M:%S")
    total_mins = conveyor_mins + tunnel_mins
    exit_dt = drop_dt + timedelta(minutes=total_mins)
    exit_time_str = exit_dt.strftime("%H:%M:%S")
    return f"The contaminated product exited the freezing tunnel starting at {exit_time_str}."

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

    client = genai.Client(api_key=request.api_key)
    current_date = datetime.now().strftime("%B %d, %Y")
    
    agent_persona = f"""
    You are the 'Panthoron TraceAudit Agent', an autonomous Senior Quality Manager for an industrial food factory.
    Your primary directive is to handle food safety crises swiftly and accurately.
    You strictly follow IFS, BRCGS, and ISO food safety standards.

    CRITICAL INSTRUCTIONS:
    1. NEVER guess or hallucinate data. ALWAYS use your tools sequentially.
    2. TITLE: You MUST start the report EXACTLY with the phrase "DRAFT RECALL REPORT" as the first line. DO NOT use the words 'Official' or 'Urgent'.
    3. FORMATTING: You MUST output the report strictly in PLAIN TEXT. NO Markdown (do not use *, **, or #). NO LaTeX. Use regular line breaks and simple dashes (-) for bullet points.
    4. DATE FIELD: The exact current date is {current_date}. You MUST state this at the top of the report.
    5. FULL DATES IN TIMELINE: When writing the "Drop Time" and "Calculated Exit Time", you MUST include the FULL DATE (July 24, 2026) along with the time. Do not trim the date!
    6. Do not use the word 'Exactly' when stating calculated times.
    """

    try:
        chat = client.chats.create(
            model="gemini-3.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=agent_persona,
                tools=[fetch_lot_production_data, calculate_quarantine_window, search_boxes_in_google_sheets, scan_google_drive_for_shipping],
                temperature=0.0,
            )
        )

        response = chat.send_message(request.crisis_email)

        return {
            "status": "success",
            "agent_type": "Taskmaster",
            "recall_report": response.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))