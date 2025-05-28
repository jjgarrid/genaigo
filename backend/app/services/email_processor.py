# services/email_processor.py

import logging
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
from tinydb import Query, where

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app.config import db
from analysis.gmail_analyzer import GmailAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailProcessor:
    """Service for automatically processing emails with AI analysis."""
    
    def __init__(self):
        self.db = db
        self.analyzer = None
        self.processing_settings = self._load_processing_settings()
        
    def _load_processing_settings(self) -> Dict[str, Any]:
        """Load email processing configuration."""
        settings_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            'config',
            'processingSettings.json'
        )
        
        default_settings = {
            "auto_analysis_enabled": True,
            "analysis_provider": os.environ.get("GENAIGO_ANALYSIS_PROVIDER", "deepseek"),
            "process_on_fetch": True,
            "batch_size": 10,
            "analysis_delay_minutes": 5,
            "include_analysis_types": ["entities", "summary", "categorization"],
            "priority_senders": [],
            "skip_analysis_for": ["automated", "notifications"]
        }
        
        try:
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
                    # Merge with defaults
                    return {**default_settings, **settings}
        except Exception as e:
            logger.warning(f"Could not load processing settings: {e}")
            
        return default_settings
    
    def _get_analyzer(self) -> GmailAnalyzer:
        """Get or create analyzer instance."""
        if self.analyzer is None:
            config = {
                "provider": self.processing_settings["analysis_provider"],
                "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
                "CLAUDE_API_KEY": os.environ.get("CLAUDE_API_KEY", ""),
                "DEEPSEEK_API_KEY": os.environ.get("DEEPSEEK_API_KEY", ""),
                "OLLAMA_MODEL": os.environ.get("OLLAMA_MODEL", "llama2"),
            }
            self.analyzer = GmailAnalyzer(config["provider"], config)
        return self.analyzer
    
    def process_unanalyzed_emails(self) -> Dict[str, Any]:
        """Process all emails that haven't been analyzed yet."""
        if not self.processing_settings.get("auto_analysis_enabled", True):
            logger.info("Auto analysis is disabled")
            return {"status": "disabled", "processed": 0}
            
        try:
            # Get all messages that haven't been analyzed
            messages_table = self.db.table("gmail_messages")
            analysis_table = self.db.table("gmail_analysis")
            
            all_messages = messages_table.all()
            analyzed_ids = {item["id"] for item in analysis_table.all()}
            
            unanalyzed_messages = [
                msg for msg in all_messages 
                if msg.get("id") not in analyzed_ids
            ]
            
            if not unanalyzed_messages:
                return {"status": "success", "processed": 0, "message": "No new messages to analyze"}
            
            logger.info(f"Found {len(unanalyzed_messages)} unanalyzed messages")
            
            # Process in batches
            batch_size = self.processing_settings.get("batch_size", 10)
            processed_count = 0
            skipped_count = 0
            errors = []
            
            for i in range(0, len(unanalyzed_messages), batch_size):
                batch = unanalyzed_messages[i:i + batch_size]
                batch_result = self._process_message_batch(batch)
                processed_count += batch_result["processed"]
                skipped_count += batch_result.get("skipped", 0)
                errors.extend(batch_result.get("errors", []))
                
            result = {
                "status": "success",
                "processed": processed_count,
                "skipped": skipped_count,
                "total_found": len(unanalyzed_messages),
                "errors": len(errors)
            }
            
            if errors:
                result["error_details"] = errors[:5]  # Include first 5 errors
                
            self._log_processing_result(result)
            return result
            
        except Exception as e:
            logger.error(f"Email processing failed: {e}")
            error_result = {"status": "error", "message": str(e)}
            self._log_processing_result(error_result)
            return error_result
    
    def _process_message_batch(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process a batch of messages."""
        analyzer = self._get_analyzer()
        processed = 0
        errors = []
        skipped = 0
        
        for msg in messages:
            try:
                msg_id = msg.get("id")
                if not msg_id:
                    logger.warning("Message missing ID, skipping")
                    skipped += 1
                    continue
                
                # Double-check that this message hasn't been processed already
                if self._is_already_processed(msg_id):
                    logger.info(f"Message {msg_id} already processed, skipping")
                    skipped += 1
                    continue
                
                if self._should_skip_analysis(msg):
                    logger.info(f"Skipping analysis for message {msg_id} (filtered out)")
                    skipped += 1
                    continue
                    
                content = msg.get("content", "") or msg.get("body", "")
                if not content.strip():
                    logger.warning(f"Empty content for message {msg_id}")
                    skipped += 1
                    continue
                    
                # Perform analysis
                logger.info(f"Starting analysis for message {msg_id}: {msg.get('subject', 'No subject')[:50]}...")
                analysis_result = analyzer.analyze(content, metadata=msg)
                
                # Store analysis result with atomic operation
                analysis_record = {
                    "id": msg_id,
                    "report": analysis_result,
                    "processed_at": datetime.utcnow().isoformat() + 'Z',
                    "processor_version": "1.0",
                    "analysis_types": self.processing_settings.get("include_analysis_types", []),
                    "message_subject": msg.get("subject", ""),
                    "message_sender": msg.get("sender", ""),
                    "analysis_provider": self.processing_settings.get("analysis_provider", "deepseek")
                }
                
                self.db.table("gmail_analysis").upsert(
                    analysis_record, 
                    where("id") == msg_id
                )
                
                processed += 1
                logger.info(f"Successfully analyzed message {msg_id}")
                
            except Exception as e:
                error_msg = f"Error analyzing message {msg.get('id', 'unknown')}: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                
        return {"processed": processed, "errors": errors, "skipped": skipped}
    
    def _should_skip_analysis(self, message: Dict[str, Any]) -> bool:
        """Determine if a message should be skipped for analysis."""
        sender = message.get("sender", "").lower()
        subject = message.get("subject", "").lower()
        
        # Skip based on sender patterns
        skip_patterns = self.processing_settings.get("skip_analysis_for", [])
        for pattern in skip_patterns:
            if pattern.lower() in sender or pattern.lower() in subject:
                return True
                
        # Check if it's a priority sender (never skip these)
        priority_senders = self.processing_settings.get("priority_senders", [])
        if sender in [p.lower() for p in priority_senders]:
            return False
            
        return False
    
    def _is_already_processed(self, message_id: str) -> bool:
        """Check if a specific message has already been processed."""
        try:
            analysis_table = self.db.table("gmail_analysis")
            existing = analysis_table.get(where("id") == message_id)
            return existing is not None
        except Exception as e:
            logger.error(f"Error checking if message {message_id} is processed: {e}")
            return False  # Err on the side of processing if we can't check
    
    def process_specific_emails(self, email_ids: List[str]) -> Dict[str, Any]:
        """Process specific emails by ID."""
        if not email_ids:
            return {"status": "error", "message": "No email IDs provided"}
            
        try:
            messages_table = self.db.table("gmail_messages")
            messages = []
            
            for email_id in email_ids:
                msg = messages_table.get(where("id") == email_id)
                if msg:
                    messages.append(msg)
                else:
                    logger.warning(f"Message not found: {email_id}")
            
            if not messages:
                return {"status": "error", "message": "No valid messages found"}
                
            result = self._process_message_batch(messages)
            return {
                "status": "success",
                "processed": result["processed"],
                "requested": len(email_ids),
                "found": len(messages),
                "errors": len(result.get("errors", []))
            }
            
        except Exception as e:
            logger.error(f"Specific email processing failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_analysis_stats(self) -> Dict[str, Any]:
        """Get statistics about analyzed emails."""
        try:
            messages_table = self.db.table("gmail_messages")
            analysis_table = self.db.table("gmail_analysis")
            
            total_messages = len(messages_table.all())
            analyzed_messages = len(analysis_table.all())
            
            # Get recent analysis activity
            recent_analysis = analysis_table.all()[-10:] if analysis_table.all() else []
            
            return {
                "total_messages": total_messages,
                "analyzed_messages": analyzed_messages,
                "unanalyzed_messages": total_messages - analyzed_messages,
                "analysis_coverage": (analyzed_messages / total_messages * 100) if total_messages > 0 else 0,
                "recent_analysis": recent_analysis,
                "auto_analysis_enabled": self.processing_settings.get("auto_analysis_enabled", True),
                "analysis_provider": self.processing_settings.get("analysis_provider", "deepseek")
            }
            
        except Exception as e:
            logger.error(f"Failed to get analysis stats: {e}")
            return {"error": str(e)}
    
    def _log_processing_result(self, result: Dict[str, Any]):
        """Log processing results to file."""
        try:
            log_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                'data'
            )
            log_file = os.path.join(log_dir, 'email_processing_log.json')
            
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
            logger.error(f"Failed to log processing result: {e}")

    def update_processing_settings(self, new_settings: Dict[str, Any]) -> Dict[str, Any]:
        """Update processing settings."""
        try:
            settings_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
                'config',
                'processingSettings.json'
            )
            
            # Merge with current settings
            current_settings = self.processing_settings.copy()
            current_settings.update(new_settings)
            
            # Write to file
            os.makedirs(os.path.dirname(settings_path), exist_ok=True)
            with open(settings_path, 'w') as f:
                json.dump(current_settings, f, indent=2)
                
            # Update in memory
            self.processing_settings = current_settings
            
            # Reset analyzer if provider changed
            if "analysis_provider" in new_settings:
                self.analyzer = None
                
            return {"status": "success", "message": "Settings updated successfully"}
            
        except Exception as e:
            logger.error(f"Failed to update processing settings: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_processed_email_count(self) -> int:
        """Get the number of emails that have been processed."""
        try:
            analysis_table = self.db.table("gmail_analysis")
            return len(analysis_table.all())
        except Exception as e:
            logger.error(f"Error getting processed email count: {e}")
            return 0
    
    def cleanup_duplicate_analysis(self) -> Dict[str, Any]:
        """Clean up any duplicate analysis records."""
        try:
            analysis_table = self.db.table("gmail_analysis")
            all_analysis = analysis_table.all()
            
            # Group by ID
            seen_ids = set()
            duplicates = []
            
            for record in all_analysis:
                record_id = record.get("id")
                if record_id in seen_ids:
                    duplicates.append(record)
                else:
                    seen_ids.add(record_id)
            
            # Remove duplicates (keep the most recent one)
            if duplicates:
                logger.info(f"Found {len(duplicates)} duplicate analysis records")
                for duplicate in duplicates:
                    analysis_table.remove(doc_ids=[duplicate.doc_id])
                
            return {
                "status": "success",
                "duplicates_removed": len(duplicates),
                "message": f"Removed {len(duplicates)} duplicate analysis records"
            }
            
        except Exception as e:
            logger.error(f"Error cleaning up duplicates: {e}")
            return {"status": "error", "message": str(e)}
    
    def reprocess_failed_emails(self) -> Dict[str, Any]:
        """Reprocess emails that had analysis errors."""
        try:
            # Get emails that exist but have no analysis or failed analysis
            messages_table = self.db.table("gmail_messages")
            analysis_table = self.db.table("gmail_analysis")
            
            all_messages = messages_table.all()
            all_analysis = analysis_table.all()
            
            # Find messages with failed analysis (empty or error reports)
            failed_ids = []
            for analysis in all_analysis:
                report = analysis.get("report", {})
                if not report or report.get("error") or not report.get("summary"):
                    failed_ids.append(analysis.get("id"))
            
            # Get the actual message records
            failed_messages = [
                msg for msg in all_messages 
                if msg.get("id") in failed_ids
            ]
            
            if not failed_messages:
                return {"status": "success", "processed": 0, "message": "No failed analyses to reprocess"}
            
            logger.info(f"Reprocessing {len(failed_messages)} failed analyses")
            
            # Remove existing failed analysis records
            for failed_id in failed_ids:
                analysis_table.remove(where("id") == failed_id)
            
            # Reprocess the messages
            result = self._process_message_batch(failed_messages)
            
            return {
                "status": "success",
                "reprocessed": result["processed"],
                "failed_count": len(failed_messages),
                "errors": len(result.get("errors", []))
            }
            
        except Exception as e:
            logger.error(f"Error reprocessing failed emails: {e}")
            return {"status": "error", "message": str(e)}
