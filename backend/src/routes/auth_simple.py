"""
Simple mock auth routes for testing.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/api/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    user: dict
    token: str

@router.post("/login", response_model=AuthResponse)
async def login(data: LoginRequest):
    """Mock login endpoint."""
    if len(data.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters"
        )
    
    return AuthResponse(
        user={"id": "1", "email": data.email},
        token="mock-jwt-token"
    )

@router.post("/register", response_model=AuthResponse)
async def register(data: LoginRequest):
    """Mock register endpoint."""
    if len(data.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters"
        )
    
    return AuthResponse(
        user={"id": "1", "email": data.email},
        token="mock-jwt-token"
    )