# Development Guide

## Prerequisites

- Python 3.8+
- Node.js 16+
- Gmail account with API access

## Project Setup

1. Clone the repository
2. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

## Backend Development

### Directory Structure
```
backend/
├── app/
│   ├── main.py          # FastAPI application entry point
│   ├── routes/          # API route definitions
│   └── services/        # Business logic
├── requirements.txt     # Python dependencies
└── setup_gmail.py       # Gmail OAuth setup utility
```

### Running the Backend
```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Code Structure
- `main.py` initializes the FastAPI app and includes routers
- `routes/` contains API endpoint definitions
- `services/` contains business logic (Gmail fetcher, scheduler)

## Frontend Development

### Directory Structure
```
frontend/
├── src/
│   ├── pages/           # Page components
│   ├── components/      # Reusable components
│   ├── contexts/        # React contexts
│   ├── config/          # Configuration files
│   └── App.jsx          # Main application component
├── package.json         # Dependencies and scripts
└── vite.config.js       # Vite configuration
```

### Running the Frontend
```bash
cd frontend
npm run dev
```

### Code Structure
- `App.jsx` defines the main application routes
- `pages/` contains the main page components
- `components/` contains reusable UI components
- `contexts/` contains React context providers
- `config/` contains configuration files

## Testing

### Backend Tests
Run the Gmail integration test suite:
```bash
cd backend
python ../test_gmail_integration.py
```

### Manual Testing
1. Start both backend and frontend servers
2. Access the frontend at http://localhost:5173
3. Navigate to the Gmail page to check integration status
4. Use the API documentation at http://localhost:8000/docs for direct API testing

## Adding New Features

### Backend
1. Add new routes in `backend/app/routes/`
2. Implement business logic in `backend/app/services/`
3. Update API documentation in `docs/api.md`

### Frontend
1. Add new pages in `frontend/src/pages/`
2. Create reusable components in `frontend/src/components/`
3. Update routing in `frontend/src/App.jsx`

## Code Style

### Python
- Follow PEP 8 guidelines
- Use type hints where possible
- Write docstrings for public functions and classes

### JavaScript/React
- Follow Airbnb JavaScript style guide
- Use functional components with hooks
- Write JSDoc comments for complex functions

## Deployment

See the [Deployment Guide](deployment.md) for detailed deployment instructions.