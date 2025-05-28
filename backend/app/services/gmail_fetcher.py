# Utility for analysis lookup
from tinydb import where

def get_analysis_report_by_id(record_id: str):
    """
    Retrieve analysis report for a Gmail message by ID from TinyDB.
    """
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'data', 'db.json')
    db = TinyDB(db_path)
    result = db.table("gmail_analysis").get(where("id") == record_id)
    if result:
        return result.get("report")
    return None
import json
import os
import hashlib
import base64
import email
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from tinydb import TinyDB, Query
from email.mime.text import MIMEText

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GmailFetcher:
    def __init__(self, config_dir: str = None):
        """Initialize Gmail fetcher with configuration."""
        self.config_dir = config_dir or os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
            'config'
        )
        self.data_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
            'data'
        )
        
        self.gmail_config = self._load_gmail_config()
        self.fetcher_settings = self._load_fetcher_settings()
        self.service = None
        
    def _load_gmail_config(self) -> Dict:
        """Load Gmail OAuth2 configuration."""
        config_path = os.path.join(self.config_dir, 'gmail.json')
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Gmail config not found at {config_path}")
            raise
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in Gmail config at {config_path}")
            raise
            
    def _load_fetcher_settings(self) -> Dict:
        """Load fetcher settings configuration."""
        settings_path = os.path.join(self.config_dir, 'fetcherSettings.json')
        try:
            with open(settings_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Fetcher settings not found at {settings_path}")
            raise
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in fetcher settings at {settings_path}")
            raise
            
    def _get_gmail_service(self):
        """Initialize and return Gmail API service."""
        if self.service:
            return self.service
            
        credentials_data = self.gmail_config.get('gmail_credentials', {})
        
        if not all([
            credentials_data.get('client_id'),
            credentials_data.get('client_secret'),
            credentials_data.get('refresh_token')
        ]):
            raise ValueError("Missing required Gmail credentials. Please configure gmail.json")
            
        creds = Credentials(
            token=credentials_data.get('access_token'),
            refresh_token=credentials_data.get('refresh_token'),
            token_uri='https://oauth2.googleapis.com/token',
            client_id=credentials_data.get('client_id'),
            client_secret=credentials_data.get('client_secret')
        )
        
        # Refresh token if needed
        if not creds.valid:
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                # Update the stored token
                self._update_access_token(creds.token)
            else:
                raise ValueError("Invalid credentials. Please re-authenticate.")
                
        self.service = build('gmail', 'v1', credentials=creds)
        return self.service
        
    def _update_access_token(self, new_token: str):
        """Update the access token in the configuration file."""
        config_path = os.path.join(self.config_dir, 'gmail.json')
        self.gmail_config['gmail_credentials']['access_token'] = new_token
        with open(config_path, 'w') as f:
            json.dump(self.gmail_config, f, indent=2)
            
    def _get_messages_db(self) -> TinyDB:
        """Get or create the messages database."""
        storage_path = self.fetcher_settings.get('storage_path', '../data/messages.json')
        if storage_path.startswith('../'):
            # Convert relative path to absolute
            db_path = os.path.join(self.data_dir, storage_path.replace('../data/', ''))
        else:
            db_path = storage_path
            
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        return TinyDB(db_path)
        
    def _build_search_query(self) -> str:
        """Build Gmail search query for recent messages."""
        lookback_hours = self.fetcher_settings.get('lookback_hours', 24)
        since_date = datetime.utcnow() - timedelta(hours=lookback_hours)
        
        # Gmail search query format: after:YYYY/MM/DD
        date_str = since_date.strftime('%Y/%m/%d')
        
        # Build sender filter
        whitelist = self.fetcher_settings.get('sender_whitelist', [])
        if whitelist:
            sender_filter = ' OR '.join([f'from:{sender}' for sender in whitelist])
            query = f'after:{date_str} ({sender_filter})'
        else:
            query = f'after:{date_str}'
            
        logger.info(f"Gmail search query: {query}")
        return query
        
    def _extract_message_data(self, message: Dict) -> Optional[Dict]:
        """Extract relevant data from a Gmail message."""
        try:
            payload = message.get('payload', {})
            headers = payload.get('headers', [])
            
            # Extract headers
            subject = None
            sender = None
            date = None
            
            for header in headers:
                name = header.get('name', '').lower()
                value = header.get('value', '')
                
                if name == 'subject':
                    subject = value
                elif name == 'from':
                    sender = value
                elif name == 'date':
                    date = value
                    
            # Extract message body
            body = self._extract_body(payload)
            
            if not all([subject, sender, date, body]):
                logger.warning(f"Missing required fields for message {message.get('id')}")
                return None
                
            # Compute body hash
            body_hash = hashlib.sha256(body.encode('utf-8')).hexdigest()
            
            return {
                'messageId': message.get('id'),
                'subject': subject,
                'sender': sender,
                'date': date,
                'retrievalTimestamp': datetime.utcnow().isoformat() + 'Z',
                'body': body,
                'bodyHash': body_hash
            }
            
        except Exception as e:
            logger.error(f"Error extracting message data: {e}")
            return None
            
    def _extract_body(self, payload: Dict) -> str:
        """Extract body content from message payload."""
        body_data = ""
        
        if 'parts' in payload:
            # Multipart message
            for part in payload['parts']:
                if part.get('mimeType') in ['text/plain', 'text/html']:
                    part_body = part.get('body', {}).get('data')
                    if part_body:
                        decoded = base64.urlsafe_b64decode(part_body).decode('utf-8')
                        body_data += decoded + "\n"
        else:
            # Single part message
            if payload.get('mimeType') in ['text/plain', 'text/html']:
                body_content = payload.get('body', {}).get('data')
                if body_content:
                    body_data = base64.urlsafe_b64decode(body_content).decode('utf-8')
                    
        return body_data.strip()
        
    def _is_sender_whitelisted(self, sender: str) -> bool:
        """Check if sender is in the whitelist."""
        whitelist = self.fetcher_settings.get('sender_whitelist', [])
        if not whitelist:
            return True  # If no whitelist, allow all
            
        # Extract email from "Name <email@domain.com>" format
        if '<' in sender and '>' in sender:
            email_part = sender.split('<')[1].split('>')[0].strip()
        else:
            email_part = sender.strip()
            
        return email_part.lower() in [w.lower() for w in whitelist]
        
    def fetch_recent_emails(self) -> Dict:
        """Main method to fetch recent emails and store them."""
        if not self.fetcher_settings.get('enabled', True):
            logger.info("Gmail fetcher is disabled")
            return {'status': 'disabled', 'processed': 0}
            
        try:
            service = self._get_gmail_service()
            query = self._build_search_query()
            
            # List messages
            result = service.users().messages().list(
                userId='me',
                q=query,
                labelIds=['INBOX']
            ).execute()
            
            messages = result.get('messages', [])
            logger.info(f"Found {len(messages)} messages matching criteria")
            
            if not messages:
                return {'status': 'success', 'processed': 0}
                
            # Get database
            db = self._get_messages_db()
            Message = Query()
            
            processed_count = 0
            skipped_count = 0
            
            for msg_ref in messages:
                try:
                    # Get full message
                    message = service.users().messages().get(
                        userId='me',
                        id=msg_ref['id'],
                        format='full'
                    ).execute()
                    
                    # Extract message data
                    message_data = self._extract_message_data(message)
                    if not message_data:
                        skipped_count += 1
                        continue
                        
                    # Check if sender is whitelisted
                    if not self._is_sender_whitelisted(message_data['sender']):
                        logger.info(f"Skipping message from non-whitelisted sender: {message_data['sender']}")
                        skipped_count += 1
                        continue
                        
                    # Check if message already exists (by messageId)
                    existing = db.search(Message.messageId == message_data['messageId'])
                    if existing:
                        logger.info(f"Message {message_data['messageId']} already exists, skipping")
                        skipped_count += 1
                        continue
                        
                    # Store message
                    db.insert(message_data)
                    processed_count += 1
                    logger.info(f"Stored message: {message_data['subject'][:50]}...")
                    
                except Exception as e:
                    logger.error(f"Error processing message {msg_ref.get('id')}: {e}")
                    skipped_count += 1
                    continue
                    
            logger.info(f"Processed {processed_count} new messages, skipped {skipped_count}")
            
            return {
                'status': 'success',
                'processed': processed_count,
                'skipped': skipped_count,
                'total_found': len(messages)
            }
            
        except HttpError as e:
            logger.error(f"Gmail API error: {e}")
            return {'status': 'error', 'message': str(e)}
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {'status': 'error', 'message': str(e)}
            
    def get_stored_messages(self, limit: int = 100) -> List[Dict]:
        """Retrieve stored messages from database."""
        db = self._get_messages_db()
        all_messages = db.all()
        
        # Sort by retrievalTimestamp (most recent first)
        sorted_messages = sorted(
            all_messages, 
            key=lambda x: x.get('retrievalTimestamp', ''), 
            reverse=True
        )
        
        return sorted_messages[:limit]
        
    def get_message_stats(self) -> Dict:
        """Get statistics about stored messages."""
        db = self._get_messages_db()
        all_messages = db.all()
        
        if not all_messages:
            return {
                'total_messages': 0,
                'unique_senders': 0,
                'date_range': None
            }
            
        # Count unique senders
        senders = set(msg.get('sender', '') for msg in all_messages)
        
        # Get date range
        timestamps = [msg.get('retrievalTimestamp', '') for msg in all_messages if msg.get('retrievalTimestamp')]
        timestamps.sort()
        
        date_range = None
        if timestamps:
            date_range = {
                'earliest': timestamps[0],
                'latest': timestamps[-1]
            }
            
        return {
            'total_messages': len(all_messages),
            'unique_senders': len(senders),
            'date_range': date_range,
            'senders': list(senders)
        }
