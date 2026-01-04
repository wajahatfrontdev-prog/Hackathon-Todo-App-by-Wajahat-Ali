# Todo App Quick Start

## Issues Fixed:
1. ✅ Backend server not running (causing "Failed to fetch")
2. ✅ Better error messages in chatbot
3. ✅ Startup scripts created
4. ✅ OpenAI API key placeholder added

## To Run the Application:

### Step 1: Start Backend
Double-click `start-backend.bat` or run:
```bash
cd backend
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 2: Start Frontend  
Double-click `start-frontend.bat` or run:
```bash
cd frontend
npm run dev
```

### Step 3: Configure OpenAI (Optional)
To enable AI chatbot:
1. Get API keys from https://platform.openai.com/api-keys
2. Replace `your-openai-api-key-here` in `backend/.env`
3. Restart backend

## URLs:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Troubleshooting:
- If "Failed to fetch" appears: Make sure backend is running on port 8000
- If chatbot shows welcome message: Either backend is down or OpenAI key not configured
- If database errors: Check DATABASE_URL in backend/.env