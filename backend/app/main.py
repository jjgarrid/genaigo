from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from .routes.gmail import router as gmail_router
from .routes.time import router as time_router
from .services.scheduler import get_scheduler
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="GenAI Go Backend", description="Backend API with Gmail integration")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the exact origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(gmail_router)
app.include_router(time_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    """Start the Gmail scheduler on application startup."""
    try:
        scheduler = get_scheduler()
        scheduler.start()
        logger.info("Gmail scheduler started on application startup")
    except Exception as e:
        logger.error(f"Failed to start Gmail scheduler: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Stop the Gmail scheduler on application shutdown."""
    try:
        scheduler = get_scheduler()
        scheduler.stop()
        logger.info("Gmail scheduler stopped on application shutdown")
    except Exception as e:
        logger.error(f"Failed to stop Gmail scheduler: {e}")

@app.get("/health")
def health():
    return {"status": "ok", "service": "GenAI Go Backend"}

# Keep the original time endpoint for backward compatibility
@app.get("/api/time")
def get_current_time_legacy():
    """
    Returns the current server time in ISO format (legacy endpoint)
    """
    return {"time": datetime.utcnow().isoformat() + "Z"}
