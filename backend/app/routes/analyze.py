from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import sys
import os

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from analysis.gmail_analyzer import GmailAnalyzer
from app.config import db
from app.services.email_processor import EmailProcessor
from tinydb import where
import os

router = APIRouter(prefix="/api")

# Example config - in production, load from env or config file
ANALYSIS_CONFIG = {
    "provider": os.environ.get("GENAIGO_ANALYSIS_PROVIDER", "deepseek"),
    "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
    "CLAUDE_API_KEY": os.environ.get("CLAUDE_API_KEY", ""),
    "DEEPSEEK_API_KEY": os.environ.get("DEEPSEEK_API_KEY", ""),
    "OLLAMA_MODEL": os.environ.get("OLLAMA_MODEL", "llama2"),
}

class AnalyzeRequest(BaseModel):
    ids: List[str] = []  # Optional: analyze specific message IDs

class ProcessingSettingsUpdate(BaseModel):
    auto_analysis_enabled: Optional[bool] = None
    analysis_provider: Optional[str] = None
    process_on_fetch: Optional[bool] = None
    batch_size: Optional[int] = None
    include_analysis_types: Optional[List[str]] = None
    priority_senders: Optional[List[str]] = None
    skip_analysis_for: Optional[List[str]] = None

@router.post("/analyze/gmail")
def analyze_gmail(request: AnalyzeRequest):
    """Legacy endpoint for manual analysis of specific messages."""
    analyzer = GmailAnalyzer(ANALYSIS_CONFIG["provider"], ANALYSIS_CONFIG)
    messages = db.table("gmail_messages").all()
    if request.ids:
        messages = [m for m in messages if m.get("id") in request.ids]
    reports = []
    for msg in messages:
        content = msg.get("content", "") or msg.get("body", "")
        report = analyzer.analyze(content, metadata=msg)
        db.table("gmail_analysis").upsert({"id": msg["id"], "report": report}, doc_ids=[msg.doc_id])
        reports.append({"id": msg["id"], "report": report})
    return {"reports": reports}

@router.get("/analysis/gmail/{id}")
def get_gmail_analysis(id: str):
    """Get analysis for a specific email."""
    result = db.table("gmail_analysis").get(where("id") == id)
    if not result:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return result["report"]

# New automatic processing endpoints

@router.post("/process/emails/auto")
async def process_emails_automatically(background_tasks: BackgroundTasks):
    """Trigger automatic processing of all unanalyzed emails."""
    processor = EmailProcessor()
    
    # Run processing in background
    background_tasks.add_task(processor.process_unanalyzed_emails)
    
    return {
        "status": "started", 
        "message": "Email processing started in background"
    }

@router.post("/process/emails/now")
async def process_emails_now():
    """Process all unanalyzed emails immediately."""
    processor = EmailProcessor()
    result = processor.process_unanalyzed_emails()
    return result

@router.post("/process/emails/specific")
async def process_specific_emails(request: AnalyzeRequest):
    """Process specific emails by ID."""
    if not request.ids:
        raise HTTPException(status_code=400, detail="No email IDs provided")
        
    processor = EmailProcessor()
    result = processor.process_specific_emails(request.ids)
    return result

@router.get("/analysis/stats")
async def get_analysis_statistics():
    """Get analysis statistics and coverage."""
    processor = EmailProcessor()
    stats = processor.get_analysis_stats()
    if "error" in stats:
        raise HTTPException(status_code=500, detail=stats["error"])
    return stats

@router.get("/analysis/processed")
async def get_processed_emails(limit: int = 50):
    """Get list of processed emails with their analysis."""
    try:
        analysis_table = db.table("gmail_analysis")
        messages_table = db.table("gmail_messages")
        
        # Get recent analysis results
        recent_analysis = analysis_table.all()[-limit:] if analysis_table.all() else []
        
        # Enrich with message metadata
        enriched_results = []
        for analysis in recent_analysis:
            message = messages_table.get(where("id") == analysis["id"])
            if message:
                enriched_results.append({
                    "id": analysis["id"],
                    "subject": message.get("subject", ""),
                    "sender": message.get("sender", ""),
                    "date": message.get("date", ""),
                    "processed_at": analysis.get("processed_at", ""),
                    "analysis": analysis.get("report", {}),
                    "analysis_types": analysis.get("analysis_types", [])
                })
                
        return {"processed_emails": enriched_results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/processing/settings")
async def get_processing_settings():
    """Get current email processing settings."""
    processor = EmailProcessor()
    return processor.processing_settings

@router.put("/processing/settings")
async def update_processing_settings(settings: ProcessingSettingsUpdate):
    """Update email processing settings."""
    processor = EmailProcessor()
    
    # Convert Pydantic model to dict, excluding None values
    update_data = {k: v for k, v in settings.dict().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No settings provided to update")
        
    result = processor.update_processing_settings(update_data)
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
        
    return result

@router.get("/processing/logs")
async def get_processing_logs(limit: int = 20):
    """Get recent email processing logs."""
    try:
        import json
        log_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            'data',
            'email_processing_log.json'
        )
        
        if not os.path.exists(log_file):
            return {"logs": []}
            
        with open(log_file, 'r') as f:
            logs = json.load(f)
            
        # Return the most recent logs
        recent_logs = logs[-limit:] if logs else []
        return {"logs": recent_logs}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process/emails/cleanup-duplicates")
def cleanup_duplicate_analysis():
    """Clean up duplicate analysis records."""
    try:
        processor = EmailProcessor()
        result = processor.cleanup_duplicate_analysis()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process/emails/reprocess-failed")
def reprocess_failed_emails():
    """Reprocess emails that had analysis errors."""
    try:
        processor = EmailProcessor()
        result = processor.reprocess_failed_emails()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analysis/processed-count")
def get_processed_count():
    """Get the number of processed emails."""
    try:
        processor = EmailProcessor()
        count = processor.get_processed_email_count()
        return {"processed_count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
