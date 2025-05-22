from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the exact origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return "ok"

@app.get("/api/time")
def get_current_time():
    """
    Returns the current server time in ISO format
    """
    return {"time": datetime.utcnow().isoformat() + "Z"}
