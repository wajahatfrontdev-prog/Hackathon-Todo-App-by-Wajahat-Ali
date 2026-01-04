@echo off
echo Starting Todo App Backend...
cd backend
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
pause