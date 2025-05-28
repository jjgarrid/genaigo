#!/bin/bash

# GenAI Go - Startup Script
# This script starts both the backend and frontend servers

set -e  # Exit on any error

echo "🚀 Starting GenAI Go Application..."
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to kill processes on specific ports
kill_port() {
    local port=$1
    local pids=$(lsof -ti :$port)
    if [ ! -z "$pids" ]; then
        print_warning "Killing existing processes on port $port"
        kill -9 $pids 2>/dev/null || true
        sleep 2
    fi
}

# Cleanup function
cleanup() {
    print_warning "Shutting down servers..."
    kill_port 8000  # Backend
    kill_port 5173  # Frontend (Vite default)
    kill_port 3000  # Frontend (alternative)
    exit 0
}

# Set up signal handlers for graceful shutdown
trap cleanup SIGINT SIGTERM

# Check if we're in the right directory
if [ ! -f "start.sh" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

print_status "Checking project structure..."

# Verify required directories exist
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "Missing backend or frontend directory"
    exit 1
fi

if [ ! -f "backend/requirements.txt" ] || [ ! -f "frontend/package.json" ]; then
    print_error "Missing required configuration files"
    exit 1
fi

print_success "Project structure verified"

# Check and install Python dependencies
print_status "Setting up backend dependencies..."
cd backend

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required but not installed"
    exit 1
fi

# Install Python dependencies
print_status "Installing Python dependencies..."
pip3 install -r requirements.txt --quiet

print_success "Backend dependencies installed"
cd ..

# Check and install Node.js dependencies
print_status "Setting up frontend dependencies..."
cd frontend

# Check if npm is available
if ! command -v npm &> /dev/null; then
    print_error "npm is required but not installed"
    exit 1
fi

# Install Node.js dependencies
print_status "Installing Node.js dependencies..."
npm install --silent

print_success "Frontend dependencies installed"
cd ..

# Check configuration files
print_status "Checking configuration..."

if [ ! -f "config/gmail.json" ]; then
    print_warning "Gmail configuration not found at config/gmail.json"
    print_warning "Run 'python backend/setup_gmail.py' to configure Gmail integration"
fi

if [ ! -f "config/fetcherSettings.json" ]; then
    print_warning "Fetcher settings not found at config/fetcherSettings.json"
fi

# Create data directory if it doesn't exist
mkdir -p data

print_success "Configuration check completed"

# Kill any existing processes on our ports
kill_port 8000
kill_port 5173
kill_port 3000

# Start backend server
print_status "Starting backend server on port 8000..."
cd backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Wait a bit for backend to start
sleep 3

# Check if backend started successfully
if check_port 8000; then
    print_success "Backend server started successfully"
else
    print_error "Failed to start backend server"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

# Start frontend server
print_status "Starting frontend server on port 5173..."
cd frontend
npm run dev -- --host 0.0.0.0 --port 5173 &
FRONTEND_PID=$!
cd ..

# Wait a bit for frontend to start
sleep 5

# Check if frontend started successfully
if check_port 5173; then
    print_success "Frontend server started successfully"
else
    print_error "Failed to start frontend server"
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    exit 1
fi

# Print startup information
echo ""
echo "🎉 GenAI Go is now running!"
echo "=========================="
echo ""
echo "Backend API:     http://localhost:8000"
echo "Frontend App:    http://localhost:5173"
echo "Gmail Dashboard: file://$(pwd)/gmail_dashboard.html"
echo ""
echo "API Documentation: http://localhost:8000/docs"
echo "Gmail Health:      http://localhost:8000/api/gmail/health"
echo ""
print_status "Press Ctrl+C to stop all servers"
echo ""

# Health check
print_status "Performing health checks..."

# Check backend health
sleep 2
if curl -s -f http://localhost:8000/health >/dev/null 2>&1; then
    print_success "Backend health check passed"
else
    print_warning "Backend health check failed - server may still be starting"
fi

# Check Gmail integration health
if curl -s -f http://localhost:8000/api/gmail/health >/dev/null 2>&1; then
    print_success "Gmail integration health check passed"
else
    print_warning "Gmail integration health check failed - check configuration"
fi

# Wait for user interruption
wait
