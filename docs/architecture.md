# System Architecture

## Overview

The GenAI Go Email Integration Platform consists of two main components:

1. **Backend** - A Python FastAPI application that handles Gmail integration
2. **Frontend** - A React web application that provides the user interface

## Backend Architecture

The backend is built with FastAPI and consists of:

### Core Services
- **Gmail Fetcher** (`backend/app/services/gmail_fetcher.py`) - Handles all Gmail API interactions
- **Scheduler** (`backend/app/services/scheduler.py`) - Manages automated email fetching

### API Routes
- **Gmail Routes** (`backend/app/routes/gmail.py`) - Endpoints for Gmail integration
- **Time Routes** (`backend/app/routes/time.py`) - Time-related endpoints

### Data Storage
- **TinyDB** - Lightweight JSON database for storing email messages
- **File-based storage** - Data stored in `data/messages.json`

## Frontend Architecture

The frontend is a React application with:

### Pages
- **Landing Page** - Main dashboard
- **Gmail Page** - Gmail integration management
- **Settings Page** - Configuration management

### Components
- **Layout** - Common page structure
- **TimeWidget** - Current time display
- **UI Components** - Reusable interface elements

## Data Flow

1. User configures Gmail credentials and fetcher settings
2. Scheduler runs periodically based on cron schedule
3. Gmail Fetcher queries Gmail API for new messages
4. Messages are filtered by sender whitelist
5. New messages are stored in TinyDB
6. Frontend displays messages and statistics via API