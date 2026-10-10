from fastapi import FastAPI
from datetime import datetime
from zoneinfo import ZoneInfo

app = FastAPI()

@app.get("/")
def home():
    return {
        "project": "RTD Commute Tracker",
        "status": "running",
        "current_time": datetime.now(
            ZoneInfo("America/Denver")
        ).isoformat()
    }
