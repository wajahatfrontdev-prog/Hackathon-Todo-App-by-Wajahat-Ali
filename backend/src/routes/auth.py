"""
Authentication routes for user registration and login.
"""

from datetime import datetime, timedelta
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_db
from ..models import User

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = "my-super-secret-jwt-key-for-phase2-2025-dont-share-this"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    user: dict
    token: str


def create_access_token(user_id: str) -> str:
    """Create JWT access token."""
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode = {"sub": user_id, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register", response_model=AuthResponse)
async def register(
    data: RegisterRequest,
    session: Annotated[AsyncSession, Depends(get_db)],
):
    """Register a new user."""
    # Check if user exists
    result = await session.execute(select(User).where(User.email == data.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Create new user
    hashed_password = pwd_context.hash(data.password)
    user = User(email=data.email, hashed_password=hashed_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    
    # Create token
    token = create_access_token(str(user.id))
    
    return AuthResponse(
        user={"id": str(user.id), "email": user.email},
        token=token,
    )


@router.post("/login", response_model=AuthResponse)
async def login(
    data: LoginRequest,
    session: Annotated[AsyncSession, Depends(get_db)],
):
    """Login user."""
    # Find user
    result = await session.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    
    if not user or not pwd_context.verify(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    # Create token
    token = create_access_token(str(user.id))
    
    return AuthResponse(
        user={"id": str(user.id), "email": user.email},
        token=token,
    )
