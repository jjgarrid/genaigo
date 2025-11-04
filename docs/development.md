# Development Guide

This guide provides instructions for setting up and running the GenAI Go Email Integration Platform for development purposes.

## 🚀 Quick Start

For a fast and easy setup, use the provided npm scripts from the root directory.

### 1. Install All Dependencies
This command installs both backend (pip) and frontend (npm) dependencies.
```bash
npm run setup
```

### 2. Run Both Servers
This command starts both the backend and frontend servers concurrently.
```bash
npm run start:dev
```
-   **Backend** will be available at `http://localhost:8000`
-   **Frontend** will be available at `http://localhost:5173`

## 📋 Prerequisites

-   **Python 3.8+** with `pip`
-   **Node.js 16+** with `npm`
-   A **Gmail account** with API access enabled.

## ⚙️ Configuration

Before running the application, you must configure the Gmail API and fetcher settings.

### 1. Gmail API Setup
Run the guided OAuth2 setup script:
```bash
npm run setup:gmail
```
This script will:
-   Guide you through creating Google Cloud credentials.
-   Handle the OAuth2 authorization flow.
-   Save the final credentials to `config/gmail.json`.

### 2. Fetcher Settings
Edit `config/fetcherSettings.json` to control the email fetching behavior:
```json
{
  "sender_whitelist": [
    "your-sender@example.com"
  ],
  "schedule": "0 2 * * *",
  "enabled": true,
  "lookback_hours": 24
}
```

## 🔧 Manual Server Management

If you prefer to run the servers individually:

### Backend Server
```bash
# From the root directory
npm run backend
```
Or manually:
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Server
```bash
# From the root directory
npm run frontend
```
Or manually:
```bash
cd frontend
npm run dev
```

## 🧪 Testing

### Automated Tests
Run the Python-based Gmail integration test suite:
```bash
npm run test
```
This script executes `test_gmail_integration.py` to validate the backend functionality.

### Manual Testing
1.  **Web Interface**: Access the frontend at `http://localhost:5173` to interact with the application.
2.  **API Docs**: Use the interactive Swagger UI at `http://localhost:8000/docs` to test API endpoints directly.
3.  **Standalone Dashboard**: Open `gmail_dashboard.html` in a browser for a simple, dependency-free interface to test the backend.

## 📁 Project Structure

For a detailed breakdown of the project structure, refer to the [Architecture Documentation](architecture.md).

## 🎨 Code Style

### Python (Backend)
-   Follow **PEP 8** guidelines for code formatting.
-   Use type hints for function signatures.
-   Write clear docstrings for all public modules, classes, and functions.

### JavaScript/React (Frontend)
-   Follow the **Airbnb JavaScript style guide**.
-   Use functional components with React Hooks.
-   Write JSDoc comments for complex functions and components.

## 🚢 Deployment

For instructions on deploying the application to a production environment, see the [Deployment Guide](deployment.md).
