from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Optional
from pydantic import BaseModel
import logging
from ..services.gmail_fetcher import GmailFetcher
from ..services.scheduler import get_scheduler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/gmail", tags=["gmail"])

# Pydantic models for request/response
class FetchResult(BaseModel):
    status: str
    processed: int
    skipped: Optional[int] = None
    total_found: Optional[int] = None
    message: Optional[str] = None

class MessageData(BaseModel):
    messageId: str
    subject: str
    sender: str
    date: str
    retrievalTimestamp: str
    body: str
    bodyHash: str

class MessageStats(BaseModel):
    total_messages: int
    unique_senders: int
    date_range: Optional[Dict] = None
    senders: List[str] = []

class SchedulerInfo(BaseModel):
    running: bool
    next_run_time: Optional[str] = None
    schedule: str

class JobLog(BaseModel):
    timestamp: str
    result: Dict

@router.get("/health")
async def gmail_health():
    """Check if Gmail fetcher is properly configured."""
    try:
        fetcher = GmailFetcher()
        # Try to initialize (this will check credentials)
        service = fetcher._get_gmail_service()
        return {"status": "healthy", "configured": True}
    except ValueError as e:
        return {"status": "unhealthy", "configured": False, "error": str(e)}
    except Exception as e:
        return {"status": "unhealthy", "configured": False, "error": f"Unexpected error: {str(e)}"}

@router.post("/fetch", response_model=FetchResult)
async def fetch_emails_now():
    """Manually trigger email fetching."""
    try:
        fetcher = GmailFetcher()
        result = fetcher.fetch_recent_emails()
        return FetchResult(**result)
    except Exception as e:
        logger.error(f"Manual fetch failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/messages", response_model=List[MessageData])
async def get_messages(limit: int = 100):
    """Get stored messages."""
    try:
        fetcher = GmailFetcher()
        messages = fetcher.get_stored_messages(limit=limit)
        return [MessageData(**msg) for msg in messages]
    except Exception as e:
        logger.error(f"Failed to get messages: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats", response_model=MessageStats)
async def get_message_stats():
    """Get message statistics."""
    try:
        fetcher = GmailFetcher()
        stats = fetcher.get_message_stats()
        return MessageStats(**stats)
    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/scheduler", response_model=SchedulerInfo)
async def get_scheduler_info():
    """Get scheduler information."""
    try:
        scheduler = get_scheduler()
        fetcher = GmailFetcher()
        
        return SchedulerInfo(
            running=scheduler.running,
            next_run_time=scheduler.get_next_run_time(),
            schedule=fetcher.fetcher_settings.get('schedule', '0 2 * * *')
        )
    except Exception as e:
        logger.error(f"Failed to get scheduler info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/scheduler/start")
async def start_scheduler():
    """Start the email scheduler."""
    try:
        scheduler = get_scheduler()
        scheduler.start()
        return {"status": "started", "message": "Gmail scheduler started successfully"}
    except Exception as e:
        logger.error(f"Failed to start scheduler: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/scheduler/stop")
async def stop_scheduler():
    """Stop the email scheduler."""
    try:
        scheduler = get_scheduler()
        scheduler.stop()
        return {"status": "stopped", "message": "Gmail scheduler stopped successfully"}
    except Exception as e:
        logger.error(f"Failed to stop scheduler: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/scheduler/run-now", response_model=FetchResult)
async def run_scheduler_now():
    """Manually trigger the scheduled job."""
    try:
        scheduler = get_scheduler()
        result = scheduler.run_now()
        return FetchResult(**result)
    except Exception as e:
        logger.error(f"Failed to run scheduler job: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/scheduler/logs", response_model=List[JobLog])
async def get_scheduler_logs(limit: int = 10):
    """Get recent scheduler job logs."""
    try:
        scheduler = get_scheduler()
        logs = scheduler.get_job_logs(limit=limit)
        return [JobLog(**log) for log in logs]
    except Exception as e:
        logger.error(f"Failed to get scheduler logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/config")
async def get_gmail_config():
    """Get current Gmail fetcher configuration (without sensitive data)."""
    try:
        fetcher = GmailFetcher()
        settings = fetcher.fetcher_settings.copy()
        
        # Add some additional info
        config_info = {
            "settings": settings,
            "credentials_configured": bool(
                fetcher.gmail_config.get('gmail_credentials', {}).get('client_id') and
                fetcher.gmail_config.get('gmail_credentials', {}).get('client_secret') and
                fetcher.gmail_config.get('gmail_credentials', {}).get('refresh_token')
            )
        }
        
        return config_info
    except Exception as e:
        logger.error(f"Failed to get config: {e}")
        raise HTTPException(status_code=500, detail=str(e))
