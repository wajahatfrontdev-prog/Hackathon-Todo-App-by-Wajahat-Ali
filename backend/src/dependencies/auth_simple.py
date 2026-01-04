"""
Simple mock auth dependencies.
"""

import hashlib
from uuid import UUID
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UUID:
    """Mock auth dependency that generates unique UUID per token."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    # Generate unique UUID from token
    token_hash = hashlib.md5(credentials.credentials.encode()).hexdigest()
    user_uuid = f"{token_hash[:8]}-{token_hash[8:12]}-{token_hash[12:16]}-{token_hash[16:20]}-{token_hash[20:32]}"
    return UUID(user_uuid)
