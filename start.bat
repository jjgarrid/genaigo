@echo off
REM GenAI Go - Windows Startup Script
REM This script starts both the backend and frontend servers

setlocal EnableDelayedExpansion

echo.
echo 🚀 Starting GenAI Go Application...
echo ==================================
echo.

REM Check if we're in the right directory
if not exist "start.bat" (
    echo [ERROR] Please run this script from the project root directory
    pause
    exit /b 1
)

echo [INFO] Checking project structure...

REM Verify required directories exist
if not exist "backend\" (
    echo [ERROR] Missing backend directory
    pause
    exit /b 1
)

if not exist "frontend\" (
    echo [ERROR] Missing frontend directory
    pause
    exit /b 1
)

if not exist "backend\requirements.txt" (
    echo [ERROR] Missing backend\requirements.txt
    pause
    exit /b 1
)

if not exist "frontend\package.json" (
    echo [ERROR] Missing frontend\package.json
    pause
    exit /b 1
)

echo [SUCCESS] Project structure verified

REM Kill any existing processes on our ports
echo [INFO] Stopping any existing servers...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do taskkill /f /pid %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5173" ^| find "LISTENING"') do taskkill /f /pid %%a >nul 2>&1

REM Install backend dependencies
echo [INFO] Setting up backend dependencies...
cd backend
python -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install Python dependencies
    pause
    exit /b 1
)
echo [SUCCESS] Backend dependencies installed
cd ..

REM Install frontend dependencies
echo [INFO] Setting up frontend dependencies...
cd frontend
call npm install --silent
if errorlevel 1 (
    echo [ERROR] Failed to install Node.js dependencies
    pause
    exit /b 1
)
echo [SUCCESS] Frontend dependencies installed
cd ..

REM Check configuration files
echo [INFO] Checking configuration...
if not exist "config\gmail.json" (
    echo [WARNING] Gmail configuration not found at config\gmail.json
    echo [WARNING] Run 'python backend\setup_gmail.py' to configure Gmail integration
)

if not exist "config\fetcherSettings.json" (
    echo [WARNING] Fetcher settings not found at config\fetcherSettings.json
)

REM Create data directory if it doesn't exist
if not exist "data\" mkdir data

echo [SUCCESS] Configuration check completed

REM Start backend server
echo [INFO] Starting backend server on port 8000...
cd backend
start "GenAI Go Backend" cmd /c "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
cd ..

REM Wait for backend to start
timeout /t 5 /nobreak >nul

REM Start frontend server
echo [INFO] Starting frontend server on port 5173...
cd frontend
start "GenAI Go Frontend" cmd /c "npm run dev -- --host 0.0.0.0 --port 5173"
cd ..

REM Wait for frontend to start
timeout /t 5 /nobreak >nul

REM Print startup information
echo.
echo 🎉 GenAI Go is now running!
echo ==========================
echo.
echo Backend API:     http://localhost:8000
echo Frontend App:    http://localhost:5173
echo Gmail Dashboard: file:///%CD%/gmail_dashboard.html
echo.
echo API Documentation: http://localhost:8000/docs
echo Gmail Health:      http://localhost:8000/api/gmail/health
echo.
echo [INFO] Two command windows have been opened for the servers
echo [INFO] Close those windows to stop the servers
echo.

REM Open browser to frontend
start http://localhost:5173

echo Press any key to exit this window...
pause >nul
