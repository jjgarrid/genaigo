# API Reference

## Base URL

All API endpoints are prefixed with `/api`. The base URL is:
```
http://localhost:8000/api
```

## Health Endpoints

### GET `/health`

Returns the overall health status of the backend service.

**Response:**
```json
{
  "status": "ok",
  "service": "GenAI Go Backend"
}
```

### GET `/api/gmail/health`

Returns the health status of the Gmail integration.

**Response (success):**
```json
{
  "status": "healthy",
  "configured": true
}
```

**Response (error):**
```json
{
  "status": "unhealthy",
  "configured": false,
  "error": "Error message"
}
```

## Gmail Integration Endpoints

### POST `/api/gmail/fetch`

Manually trigger email fetching.

**Response:**
```json
{
  "status": "success",
  "processed": 5,
  "skipped": 2,
  "total_found": 7
}
```

### GET `/api/gmail/messages`

Get stored messages.

**Query Parameters:**
- `limit` (optional, default: 100) - Maximum number of messages to return

**Response:**
```json
[
  {
    "messageId": "12345",
    "subject": "Email Subject",
    "sender": "sender@example.com",
    "date": "2023-01-01T10:00:00Z",
    "retrievalTimestamp": "2023-01-01T10:00:00Z",
    "body": "Email body content...",
    "bodyHash": "hashvalue"
  }
]
```

### GET `/api/gmail/stats`

Get message statistics.

**Response:**
```json
{
  "total_messages": 42,
  "unique_senders": 15,
  "date_range": {
    "earliest": "2023-01-01T10:00:00Z",
    "latest": "2023-01-15T14:30:00Z"
  },
  "senders": [
    "sender1@example.com",
    "sender2@example.com"
  ]
}
```

### GET `/api/gmail/scheduler`

Get scheduler information.

**Response:**
```json
{
  "running": true,
  "next_run_time": "2023-01-16T02:00:00Z",
  "schedule": "0 2 * * *"
}
```

### POST `/api/gmail/scheduler/start`

Start the email scheduler.

**Response:**
```json
{
  "status": "started",
  "message": "Gmail scheduler started successfully"
}
```

### POST `/api/gmail/scheduler/stop`

Stop the email scheduler.

**Response:**
```json
{
  "status": "stopped",
  "message": "Gmail scheduler stopped successfully"
}
```

### POST `/api/gmail/scheduler/run-now`

Manually trigger the scheduled job.

**Response:**
```json
{
  "status": "success",
  "processed": 3,
  "skipped": 1,
  "total_found": 4
}
```

### GET `/api/gmail/scheduler/logs`

Get recent scheduler job logs.

**Query Parameters:**
- `limit` (optional, default: 10) - Maximum number of logs to return

**Response:**
```json
[
  {
    "timestamp": "2023-01-15T02:00:00Z",
    "result": {
      "status": "success",
      "processed": 5,
      "skipped": 2,
      "total_found": 7
    }
  }
]
```

### GET `/api/gmail/config`

Get current Gmail fetcher configuration (without sensitive data).

**Response:**
```json
{
  "settings": {
    "sender_whitelist": ["sender@example.com"],
    "schedule": "0 2 * * *",
    "storage_path": "../data/messages.json",
    "enabled": true,
    "lookback_hours": 24
  },
  "credentials_configured": true
}
```