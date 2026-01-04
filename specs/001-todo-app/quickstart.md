# Quickstart: Todo Web Application

**Feature**: 001-todo-app | **Date**: 2025-12-30

## Prerequisites

- Node.js 20+ for Next.js frontend
- Python 3.11+ for FastAPI backend
- Neon PostgreSQL account (free tier)
- Git

## Setup

### 1. Clone and Initialize

```bash
# Clone repository
git clone <repository-url>
cd todo-web-app

# Create feature branch
git checkout -b 001-todo-app
```

### 2. Environment Configuration

Create `.env` file in repository root:

```bash
# Copy example to create actual env file
cp .env.example .env

# Edit .env with your values
```

Contents of `.env.example`:

```bash
# Frontend (Next.js)
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-min-32-chars

# Backend (FastAPI)
DATABASE_URL=postgres://user:password@ep-xxx.us-east-1.aws.neon.tech/todoapp?sslmode=require
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
CORS_ORIGINS=http://localhost:3000
```

**Important**: BETTER_AUTH_SECRET must be identical in frontend and backend for JWT verification to work.

### 3. Database Setup

1. Create Neon PostgreSQL database at https://neon.tech
2. Copy connection string to DATABASE_URL
3. The database will be initialized automatically on first run

## Running the Application

### Backend (Terminal 1)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at http://localhost:8000
API documentation at http://localhost:8000/docs

### Frontend (Terminal 2)

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at http://localhost:3000

## Development Workflow

### Making Changes

1. Make code changes in `frontend/` or `backend/`
2. Changes auto-reload on save
3. Check browser for results

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Linting

```bash
# Backend
cd backend
ruff check .
mypy .

# Frontend
cd frontend
npm run lint
```

## Project Structure

```
todo-web-app/
├── frontend/              # Next.js application
│   ├── src/
│   │   ├── app/          # App Router pages
│   │   ├── components/   # React components
│   │   └── lib/          # Utilities
│   └── package.json
│
├── backend/               # FastAPI application
│   ├── src/
│   │   ├── main.py       # Entry point
│   │   ├── models.py     # SQLModel entities
│   │   ├── db.py         # Database connection
│   │   ├── dependencies/ # Auth dependencies
│   │   └── routes/       # API endpoints
│   └── requirements.txt
│
├── .env.example           # Environment template
└── README.md
```

## Common Issues

### CORS Errors

If frontend cannot reach backend:
- Verify CORS_ORIGINS includes http://localhost:3000
- Check backend is running on port 8000

### JWT Verification Fails

If API returns 401:
- Ensure BETTER_AUTH_SECRET is identical in frontend and backend
- Check token is being sent in Authorization: Bearer header
- Verify token hasn't expired

### Database Connection Failed

If backend cannot connect to Neon:
- Verify DATABASE_URL is correct
- Check SSL requirement (Neon requires sslmode=require)
- Ensure IP is allowlisted in Neon dashboard

## Next Steps

1. Navigate to http://localhost:3000
2. Click "Sign Up" to create an account
3. Sign in with your new account
4. Add tasks using the form
5. Test all CRUD operations

## Deployment (Future)

This quickstart is for local development. For deployment:
- Deploy backend to a Python-compatible hosting service
- Deploy frontend to Vercel or similar
- Update environment variables in production
- Set up proper database with Neon
