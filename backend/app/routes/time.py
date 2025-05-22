from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/time")
def get_current_time():
    """
    Returns the current server time in ISO format
    """
    return {"time": datetime.utcnow().isoformat() + "Z"}
