#!/usr/bin/env python3

import asyncio
import json
import uuid
from src.db import get_db_context
from src.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def test_user_creation():
    """Test creating a user directly in the database."""
    try:
        async with get_db_context() as session:
            # Create a test user
            test_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
            hashed_password = pwd_context.hash("testpassword123")
            
            user = User(email=test_email, hashed_password=hashed_password)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            
            print(f"✅ User created successfully: {user.id} - {user.email}")
            return True
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_user_creation())