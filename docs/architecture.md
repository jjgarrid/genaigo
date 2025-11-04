# System Architecture

## Overview

The GenAI Go Email Integration Platform consists of two main components:

1.  **Backend**: A Python FastAPI application that handles Gmail integration, scheduling, and data storage.
2.  **Frontend**: A React web application that provides the user interface for monitoring and control.

## Backend Architecture

The backend is a FastAPI application with a modular structure designed for handling Gmail integration.

### Directory Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app with Gmail routes
│   ├── services/
│   │   ├── gmail_fetcher.py # Core Gmail API logic
│   │   └── scheduler.py     # Background job scheduler
│   └── routes/
│       └── gmail.py         # REST API endpoints
├── setup_gmail.py           # OAuth2 setup utility
└── requirements.txt         # Dependencies
```

### Key Services

-   **GmailFetcher (`services/gmail_fetcher.py`)**:
    -   Handles all Gmail API interactions, including authentication, message searching, and retrieval.
    -   Performs data extraction, processing, and storage.
    -   Implements sender filtering and message deduplication logic.

-   **GmailScheduler (`services/scheduler.py`)**:
    -   Manages background job scheduling using a cron-based system.
    -   Handles automated, periodic execution of the email fetching process.
    -   Provides controls for manual job triggering, logging, and monitoring.

### API Routes

-   **Gmail Routes (`routes/gmail.py`)**:
    -   Exposes all functionality through a comprehensive set of RESTful endpoints.
    -   Includes endpoints for health checks, status monitoring, manual fetch triggers, and configuration management.

### Data Storage

-   **TinyDB**: A lightweight, document-oriented database.
-   **JSON File**: All email data is stored in a single JSON file at `data/messages.json`.

## Frontend Architecture

The frontend is a standard React application built with Vite, providing a user-friendly interface for the backend services.

### Key Components

-   **Pages (`frontend/src/pages`)**:
    -   **GmailPage**: The main interface for managing the Gmail integration, displaying status, logs, and stored messages.
-   **Components (`frontend/src/components`)**:
    -   Reusable UI elements for displaying data and interacting with the API.
-   **Standalone Dashboard (`gmail_dashboard.html`)**:
    -   A simple, dependency-free HTML file for quick testing and status checks of the backend API.

## Data Flow

1.  **Configuration**: The user runs `setup_gmail.py` to configure OAuth2 credentials. Fetcher settings like the sender whitelist and schedule are set in `config/fetcherSettings.json`.
2.  **Scheduled Execution**: The `GmailScheduler` triggers the `GmailFetcher` service based on the configured cron schedule.
3.  **Data Retrieval**: `GmailFetcher` authenticates with the Gmail API, queries for recent messages, and filters them against the sender whitelist.
4.  **Processing & Storage**: New messages are processed to extract relevant data, and a hash is generated for deduplication. The final data is stored in the `data/messages.json` database.
5.  **User Interaction**: The React frontend communicates with the backend's REST API to display status, trigger manual fetches, and view stored messages and logs.
