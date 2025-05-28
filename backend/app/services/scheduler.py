import schedule
import time
import threading
import json
import os
import logging
from datetime import datetime
from .gmail_fetcher import GmailFetcher

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GmailScheduler:
    def __init__(self):
        """Initialize the Gmail scheduler."""
        self.fetcher = GmailFetcher()
        self.running = False
        self.thread = None
        
    def start(self):
        """Start the scheduler in a background thread."""
        if self.running:
            logger.warning("Scheduler is already running")
            return
            
        logger.info("Starting Gmail scheduler")
        self.running = True
        
        # Schedule the job based on configuration
        settings = self.fetcher.fetcher_settings
        cron_schedule = settings.get('schedule', '0 2 * * *')  # Default: 2 AM daily
        
        # Convert cron to schedule format (simplified for common patterns)
        if cron_schedule == '0 2 * * *':  # Daily at 2 AM
            schedule.every().day.at("02:00").do(self._run_fetch_job)
        elif cron_schedule.startswith('0 */'):  # Every N hours
            hours = int(cron_schedule.split('*/')[1].split(' ')[0])
            schedule.every(hours).hours.do(self._run_fetch_job)
        else:
            # Default to daily at 2 AM if we can't parse the cron
            logger.warning(f"Unsupported cron format: {cron_schedule}, defaulting to daily at 2 AM")
            schedule.every().day.at("02:00").do(self._run_fetch_job)
            
        # Start the scheduler thread
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        
        logger.info(f"Gmail scheduler started with schedule: {cron_schedule}")
        
    def stop(self):
        """Stop the scheduler."""
        if not self.running:
            return
            
        logger.info("Stopping Gmail scheduler")
        self.running = False
        schedule.clear()
        
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)
            
    def _run_scheduler(self):
        """Run the scheduler loop."""
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                time.sleep(60)
                
    def _run_fetch_job(self):
        """Execute the Gmail fetch job."""
        logger.info("Starting scheduled Gmail fetch job")
        try:
            result = self.fetcher.fetch_recent_emails()
            logger.info(f"Gmail fetch job completed: {result}")
            
            # Log results to a file for debugging
            self._log_job_result(result)
            
        except Exception as e:
            logger.error(f"Gmail fetch job failed: {e}")
            self._log_job_result({'status': 'error', 'message': str(e)})
            
    def _log_job_result(self, result: dict):
        """Log job results to a file."""
        try:
            log_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                'data'
            )
            log_file = os.path.join(log_dir, 'gmail_fetch_log.json')
            
            log_entry = {
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'result': result
            }
            
            # Read existing log
            logs = []
            if os.path.exists(log_file):
                try:
                    with open(log_file, 'r') as f:
                        logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []
                    
            # Append new entry
            logs.append(log_entry)
            
            # Keep only the last 100 entries
            logs = logs[-100:]
            
            # Write back to file
            os.makedirs(log_dir, exist_ok=True)
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to log job result: {e}")
            
    def run_now(self):
        """Manually trigger the fetch job immediately."""
        logger.info("Manually triggering Gmail fetch job")
        return self._run_fetch_job()
        
    def get_next_run_time(self):
        """Get the next scheduled run time."""
        jobs = schedule.get_jobs()
        if not jobs:
            return None
            
        next_run = min(job.next_run for job in jobs)
        return next_run.isoformat() if next_run else None
        
    def get_job_logs(self, limit: int = 10):
        """Get recent job execution logs."""
        try:
            log_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                'data'
            )
            log_file = os.path.join(log_dir, 'gmail_fetch_log.json')
            
            if not os.path.exists(log_file):
                return []
                
            with open(log_file, 'r') as f:
                logs = json.load(f)
                
            # Return the most recent logs
            return logs[-limit:] if logs else []
            
        except Exception as e:
            logger.error(f"Failed to get job logs: {e}")
            return []

# Global scheduler instance
gmail_scheduler = None

def get_scheduler():
    """Get or create the global scheduler instance."""
    global gmail_scheduler
    if gmail_scheduler is None:
        gmail_scheduler = GmailScheduler()
    return gmail_scheduler
