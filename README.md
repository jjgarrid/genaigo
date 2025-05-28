# GenAI Go - Email Integration & AI Analysis Platform

A comprehensive email integration platform that automatically fetches and processes emails from Gmail using configurable sender whitelists and scheduling, with advanced AI-powered analysis capabilities.

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
- **AI Provider API Keys** (optional, for analysis features):
  - OpenAI API key
  - Claude (Anthropic) API key
  - DeepSeek API key
  - Local Ollama installation

## ⚙️ Configuration

### 1. Environment Variables

Copy the example environment file and configure your API keys:
```bash
cp .env.example .env
```

Then edit `.env` with your actual API keys:
```bash
# AI Provider Configuration
GENAIGO_ANALYSIS_PROVIDER=deepseek  # or openai, claude, ollama

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Claude (Anthropic) Configuration
CLAUDE_API_KEY=your_claude_api_key_here

# DeepSeek Configuration
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Ollama Configuration (for local models)
OLLAMA_MODEL=llama2
```

### 2. Gmail API Setup

Run the OAuth2 setup:
```bash
npm run setup:gmail
# or manually: cd backend && python setup_gmail.py
```

This will:
- Guide you through Google Cloud Console setup
- Handle OAuth2 authorization
- Save credentials to `config/gmail.json`

### 3. Configure Email Sources

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
| `npm run setup:dev` | Install development dependencies (testing, linting) |
| `npm run setup:gmail` | Configure Gmail OAuth2 |
| `npm run test` | Run Gmail integration tests |
| `npm run test:deepseek` | Test DeepSeek API connectivity |
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

### ✅ AI-Powered Analysis
- **Multi-Provider Support**: OpenAI GPT, Claude, DeepSeek, Ollama
- **Entity Extraction**: Automatically identify people, locations, events
- **Email Categorization**: Classify emails by type and priority
- **Content Summarization**: Generate intelligent summaries
- **Configurable Providers**: Switch between AI providers via environment variables

### ✅ Data Management
- JSON database storage
- Message deduplication
- Full-text search capabilities
- Statistics and analytics
- AI analysis results storage

### ✅ Web Interface
- Real-time status monitoring
- Manual fetch triggers
- Message browsing with AI insights
- Configuration management
- Execution logs
- AI analysis dashboard

### ✅ API Endpoints
- Health checks
- Message retrieval
- AI analysis endpoints
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
curl http://localhost:8000/health

# Gmail Integration
curl http://localhost:8000/api/gmail/health
curl http://localhost:8000/api/gmail/stats
curl http://localhost:8000/api/gmail/messages?limit=10
curl -X POST http://localhost:8000/api/gmail/fetch

# AI Analysis
curl -X POST http://localhost:8000/api/analyze/emails \
  -H "Content-Type: application/json" \
  -d '{"email_ids": ["msg_123", "msg_456"]}'

curl -X POST http://localhost:8000/api/analyze/text \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text to analyze"}'

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

**"AI Provider API key missing"**
- Add your API key to the `.env` file
- Test connectivity: `python test_deepseek_api.py`
- Verify provider configuration in environment variables

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
- **Test AI providers:** `python test_deepseek_api.py`
- **API Documentation:** http://localhost:8000/docs

## 📁 Project Structure

```
genaigo/
├── .env                  # Environment variables (AI API keys)
├── start.sh              # Linux/Mac startup script
├── start.bat             # Windows startup script  
├── package.json          # Root npm scripts
├── test_deepseek_api.py  # AI provider connectivity test
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── main.py       # FastAPI application
│   │   ├── routes/       # API endpoints
│   │   │   ├── analyze.py # AI analysis endpoints
│   │   │   ├── gmail.py   # Gmail integration
│   │   │   └── time.py    # Time utilities
│   │   └── services/     # Gmail fetcher & scheduler
│   ├── analysis/         # AI analysis system
│   │   ├── gmail_analyzer.py # Email analysis logic
│   │   ├── providers/    # AI provider adapters
│   │   │   ├── openai_adapter.py
│   │   │   ├── claude_adapter.py
│   │   │   ├── deepseek_adapter.py
│   │   │   └── ollama_adapter.py
│   │   └── report_schema.py # Analysis result schemas
│   ├── requirements.txt  # Python dependencies
│   └── setup_gmail.py    # OAuth2 setup utility
├── frontend/             # React frontend
│   ├── src/
│   │   ├── pages/        # React components
│   │   │   └── GmailPage.jsx # Gmail & AI dashboard
│   │   └── components/   # Shared UI components
│   ├── package.json      # Frontend dependencies
│   └── vite.config.js    # Vite configuration
├── config/               # Configuration files
│   ├── gmail.json        # Gmail OAuth2 credentials
│   └── fetcherSettings.json # Email fetcher settings
└── data/                 # Stored data
    ├── messages.json     # Email messages database
    └── gmail_fetch_log.json # Execution logs
```

## 🔐 Security & Privacy

- **OAuth2 Flow:** Secure Google authentication
- **Read-only Scope:** Minimal Gmail API permissions  
- **Token Management:** Automatic refresh handling
- **Local Storage:** All data stored locally
- **No Modifications:** Emails remain unchanged in Gmail
- **API Key Security:** Environment variable storage
- **Multi-Provider Support:** Choose your preferred AI provider

## 🚀 Latest Features

- **AI-Powered Email Analysis:** Extract entities, categorize, and summarize emails
- **Multi-Provider AI Support:** OpenAI, Claude, DeepSeek, and Ollama integration
- **Enhanced API Endpoints:** New analysis routes with comprehensive documentation
- **Improved Testing:** Dedicated AI provider connectivity tests
- **Better Error Handling:** Comprehensive error reporting and logging
- **Modern UI:** React-based dashboard with real-time AI insights

## 📈 Current System Status

As of the last check:
- **Total Messages:** 35
- **Unique Senders:** 15
- **Date Range:** May 28, 2025 (10:23 AM - 2:22 PM)
- **System Status:** ✅ Healthy and operational
- **AI Analysis:** ✅ Multiple providers configured
- **Backend:** ✅ Running on port 8000
- **Frontend:** ✅ Running on port 5173

The system is ready for production use with full AI analysis capabilities!
