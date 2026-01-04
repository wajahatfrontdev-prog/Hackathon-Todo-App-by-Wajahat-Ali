import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend', 'src'))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.tasks import router as tasks_router
from routes.chat import router as chat_router
from db import init_db

app = FastAPI(title="Todo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
async def startup_event():
    await init_db()

# Include routers
app.include_router(tasks_router)
app.include_router(chat_router)

@app.get("/")
def read_root():
    return {"message": "Todo API is running on Vercel!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/api/health")
def api_health():
    return {"status": "ok", "service": "todo-api"}

# This is required for Vercel
app = app