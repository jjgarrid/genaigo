# Gmail Integration

This module provides automated Gmail email fetching capabilities for the GenAI Go backend. It periodically retrieves emails from a configured Gmail account, filters them based on a sender whitelist, and stores them in a JSON database without altering their "unread" status.

## Features

- **Automated Email Fetching**: Runs on a configurable schedule (default: daily at 2 AM)
- **Sender Filtering**: Only processes emails from whitelisted senders
- **Non-Intrusive**: Emails remain unread and unmodified in Gmail
- **Deduplication**: Prevents storing duplicate messages
- **REST API**: Full API for manual control and monitoring
- **Logging**: Comprehensive logging of all operations

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Google Cloud Console Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API" and enable it
4. Create OAuth2 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Choose "Desktop application" as the application type
   - Note down your `client_id` and `client_secret`

### 3. Configure Credentials

Edit `/config/gmail.json` and add your OAuth2 credentials:

```json
{
  "gmail_credentials": {
    "client_id": "your-client-id.googleusercontent.com",
    "client_secret": "your-client-secret",
    "refresh_token": "",
    "access_token": "",
    "token_expiry": null
  }
}
```

### 4. Run OAuth2 Setup

```bash
cd backend
python setup_gmail.py
```

Follow the prompts to complete OAuth2 authorization. This will populate the `refresh_token` and `access_token` fields.

### 5. Configure Settings

Edit `/config/fetcherSettings.json`:

```json
{
  "sender_whitelist": [
    "alice@example.com",
    "alerts@service.io",
    "notifications@github.com"
  ],
  "schedule": "0 2 * * *",
  "storage_path": "../data/db.json",
  "enabled": true,
  "lookback_hours": 24
}
```

## Configuration Options

### Gmail Settings (`/config/gmail.json`)

- `client_id`: OAuth2 client ID from Google Cloud Console
- `client_secret`: OAuth2 client secret from Google Cloud Console
- `refresh_token`: Long-lived token for API access (auto-generated)
- `access_token`: Short-lived token (auto-refreshed)
- `token_expiry`: Token expiration time (auto-managed)

### Fetcher Settings (`/config/fetcherSettings.json`)

- `sender_whitelist`: Array of email addresses to process
- `schedule`: Cron expression for job scheduling (default: "0 2 * * *" = daily at 2 AM)
- `storage_path`: Path to JSON database file
- `enabled`: Enable/disable the fetcher
- `lookback_hours`: How many hours back to search for emails (default: 24)

## API Endpoints

### Health Check
```http
GET /api/gmail/health
```
Returns Gmail integration health status and configuration check.

### Manual Fetch
```http
POST /api/gmail/fetch
```
Manually trigger email fetching immediately.

### Get Messages
```http
GET /api/gmail/messages?limit=100
```
Retrieve stored messages from the database.

### Get Statistics
```http
GET /api/gmail/stats
```
Get statistics about stored messages (count, senders, date range).

### Scheduler Control
```http
GET /api/gmail/scheduler           # Get scheduler status
POST /api/gmail/scheduler/start    # Start scheduler
POST /api/gmail/scheduler/stop     # Stop scheduler
POST /api/gmail/scheduler/run-now  # Trigger job immediately
GET /api/gmail/scheduler/logs      # Get recent job logs
```

### Configuration
```http
GET /api/gmail/config
```
Get current configuration (without sensitive data).

## Data Storage

Messages are stored in `/data/db.json` with the following structure:

```json
{
  "messageId": "gmail-message-id",
  "subject": "Email subject",
  "sender": "sender@example.com",
  "date": "Thu, 1 Jan 2025 12:00:00 +0000",
  "retrievalTimestamp": "2025-01-01T12:00:00Z",
  "body": "Email body content...",
  "bodyHash": "sha256-hash-of-body"
}
```

## Logging

- Application logs: Standard Python logging to console
- Job execution logs: Stored in `/data/gmail_fetch_log.json`
- Logs include execution results, error messages, and statistics

## Security Considerations

1. **OAuth2 Tokens**: Store securely and rotate regularly
2. **Read-Only Access**: Uses minimal Gmail API scopes
3. **No Modifications**: Emails remain unchanged in Gmail
4. **Whitelist Only**: Only processes emails from approved senders

## Troubleshooting

### "Invalid credentials" Error
- Run `python setup_gmail.py` to refresh OAuth2 tokens
- Check that Gmail API is enabled in Google Cloud Console
- Verify client_id and client_secret are correct

### "No messages found" 
- Check sender whitelist configuration
- Verify emails exist in the specified time range
- Check Gmail API quota limits

### Scheduler Not Running
- Check application logs for startup errors
- Verify configuration files are valid JSON
- Ensure all dependencies are installed

## Example Usage

```python
from app.services.gmail_fetcher import GmailFetcher
from app.services.scheduler import get_scheduler

# Manual fetch
fetcher = GmailFetcher()
result = fetcher.fetch_recent_emails()
print(f"Processed {result['processed']} messages")

# Get stored messages
messages = fetcher.get_stored_messages(limit=10)
for msg in messages:
    print(f"{msg['sender']}: {msg['subject']}")

# Scheduler control
scheduler = get_scheduler()
scheduler.start()  # Start background scheduler
```

## Monitoring

Monitor the Gmail integration through:

1. **API Health Endpoint**: `/api/gmail/health`
2. **Job Logs**: `/api/gmail/scheduler/logs`
3. **Message Statistics**: `/api/gmail/stats`
4. **Application Logs**: Check console output for errors

## Development

To extend the Gmail integration:

1. **Add new message processors**: Extend `GmailFetcher._extract_message_data()`
2. **Custom scheduling**: Modify `GmailScheduler` for complex schedules
3. **Additional APIs**: Add routes to `/app/routes/gmail.py`
4. **Data transformations**: Process messages before storage
