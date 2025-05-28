# GenAI Go - Email Integration Platform

A comprehensive email integration platform that automatically fetches and processes emails from Gmail using configurable sender whitelists and scheduling.

## 🚀 Quick Start

### Option 1: One-Click Startup (Recommended)

**Linux/Mac:**
```bash
./start.sh
```

**Windows:**
```cmd
start.bat
```

**Using npm:**
```bash
npm run start
```

This will:
- Install all dependencies automatically
- Start both backend (port 8000) and frontend (port 5173) servers
- Perform health checks
- Display all relevant URLs

### Option 2: Manual Setup

**Install dependencies:**
```bash
npm run setup
```

**Start both servers with concurrently:**
```bash
npm run start:dev
```

**Or start individually:**
```bash
# Terminal 1 - Backend
npm run backend

# Terminal 2 - Frontend  
npm run frontend
```

## 📋 Prerequisites

- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **Gmail account** with API access

## ⚙️ Configuration

### 1. Gmail API Setup

Run the OAuth2 setup:
```bash
npm run setup:gmail
# or manually: cd backend && python setup_gmail.py
```

This will:
- Guide you through Google Cloud Console setup
- Handle OAuth2 authorization
- Save credentials to `config/gmail.json`

### 2. Configure Email Sources

Edit `config/fetcherSettings.json`:
```json
{
  "sender_whitelist": [
    "your-sender@example.com",
    "newsletter@company.com"
  ],
  "schedule": "0 2 * * *",
  "enabled": true,
  "lookback_hours": 24
}
```

## 🌐 Access Points

Once running, access:

- **Frontend App:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Gmail Dashboard:** Open `gmail_dashboard.html` in browser

## 🔧 Available Scripts

| Command | Description |
|---------|-------------|
| `npm run start` | Start both servers with full setup |
| `npm run start:dev` | Start both servers (requires deps installed) |
| `npm run setup` | Install all dependencies |
| `npm run setup:gmail` | Configure Gmail OAuth2 |
| `npm run test` | Run Gmail integration tests |
| `npm run backend` | Start only backend server |
| `npm run frontend` | Start only frontend server |
| `npm run build` | Build frontend for production |

## 📊 Features

### ✅ Gmail Integration
- OAuth2 authentication
- Automated email fetching
- Sender whitelist filtering
- Read-only access (non-intrusive)
- Configurable scheduling (cron format)

### ✅ Data Management
- JSON database storage
- Message deduplication
- Full-text search capabilities
- Statistics and analytics

### ✅ Web Interface
- Real-time status monitoring
- Manual fetch triggers
- Message browsing
- Configuration management
- Execution logs

### ✅ API Endpoints
- Health checks
- Message retrieval
- Statistics
- Scheduler control
- Configuration management

## 🔍 Monitoring

### Health Checks
- **Backend:** http://localhost:8000/health
- **Gmail Integration:** http://localhost:8000/api/gmail/health

### Current Status
The system is currently configured and operational with:
- ✅ **35 messages** stored from **15 unique senders**
- ✅ **Gmail API** connected and healthy
- ✅ **Scheduler** running (daily at 2 AM)
- ✅ **Web interfaces** accessible

### Key Endpoints
```bash
# Get system health
curl http://localhost:8000/api/gmail/health

# Get message statistics  
curl http://localhost:8000/api/gmail/stats

# Get recent messages
curl http://localhost:8000/api/gmail/messages?limit=10

# Manual fetch trigger
curl -X POST http://localhost:8000/api/gmail/fetch

# Scheduler control
curl http://localhost:8000/api/gmail/scheduler
curl -X POST http://localhost:8000/api/gmail/scheduler/start
curl -X POST http://localhost:8000/api/gmail/scheduler/stop
```

## 🛠️ Troubleshooting

### Common Issues

**"Port already in use"**
- The startup script automatically kills existing processes
- Or manually: `pkill -f "uvicorn\|vite"`

**"Gmail credentials not configured"**
- Run: `npm run setup:gmail`
- Follow the OAuth2 setup process

**"No messages found"**
- Check sender whitelist in `config/fetcherSettings.json`
- Verify emails exist in the specified time range
- Check Gmail API quota limits

**"Dependencies not installed"**
- Run: `npm run setup`
- Or use the full startup script: `./start.sh`

### Logs and Debugging

- **Application logs:** Check terminal output
- **Execution logs:** Available via web interface or API
- **Test integration:** `npm run test`

## 📁 Project Structure

```
genaigo/
├── start.sh              # Linux/Mac startup script
├── start.bat             # Windows startup script  
├── package.json          # Root npm scripts
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── main.py       # FastAPI application
│   │   ├── routes/       # API endpoints
│   │   └── services/     # Gmail fetcher & scheduler
│   ├── requirements.txt  # Python dependencies
│   └── setup_gmail.py    # OAuth2 setup utility
├── frontend/             # React frontend
│   ├── src/
│   │   ├── pages/        # React components
│   │   └── components/   # Shared UI components
│   ├── package.json      # Frontend dependencies
│   └── vite.config.js    # Vite configuration
├── config/               # Configuration files
│   ├── gmail.json        # Gmail OAuth2 credentials
│   └── fetcherSettings.json # Email fetcher settings
└── data/                 # Stored data
    └── messages.json     # Email messages database
```

## 🔐 Security

- **OAuth2 Flow:** Secure Google authentication
- **Read-only Scope:** Minimal Gmail API permissions  
- **Token Management:** Automatic refresh handling
- **Local Storage:** All data stored locally
- **No Modifications:** Emails remain unchanged in Gmail

## 📈 Current Data Status

As of the last check:
- **Total Messages:** 35
- **Unique Senders:** 15
- **Date Range:** May 28, 2025 (10:23 AM - 2:22 PM)
- **System Status:** ✅ Healthy and operational

The system is ready for production use!
