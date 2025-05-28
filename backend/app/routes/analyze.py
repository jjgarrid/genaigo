from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import sys
import os

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from analysis.gmail_analyzer import GmailAnalyzer
from app.config import db
from tinydb import where
import os

router = APIRouter(prefix="/api")

# Example config - in production, load from env or config file
ANALYSIS_CONFIG = {
    "provider": os.environ.get("GENAIGO_ANALYSIS_PROVIDER", "openai"),
    "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
    "CLAUDE_API_KEY": os.environ.get("CLAUDE_API_KEY", ""),
    "DEEPSEEK_API_KEY": os.environ.get("DEEPSEEK_API_KEY", ""),
    "OLLAMA_MODEL": os.environ.get("OLLAMA_MODEL", "llama2"),
}

class AnalyzeRequest(BaseModel):
    ids: List[str] = []  # Optional: analyze specific message IDs

@router.post("/analyze/gmail")
def analyze_gmail(request: AnalyzeRequest):
    analyzer = GmailAnalyzer(ANALYSIS_CONFIG["provider"], ANALYSIS_CONFIG)
    messages = db.table("gmail_messages").all()
    if request.ids:
        messages = [m for m in messages if m.get("id") in request.ids]
    reports = []
    for msg in messages:
        content = msg.get("content", "")
        report = analyzer.analyze(content, metadata=msg)
        db.table("gmail_analysis").upsert({"id": msg["id"], "report": report}, doc_ids=[msg.doc_id])
        reports.append({"id": msg["id"], "report": report})
    return {"reports": reports}

@router.get("/analysis/gmail/{id}")
def get_gmail_analysis(id: str):
    result = db.table("gmail_analysis").get(where("id") == id)
    if not result:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return result["report"]
