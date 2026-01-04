"""
SQLModel database models for User entities.

This module defines:
- User: SQLModel table for user accounts
"""

from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field as SQLField, SQLModel


class User(SQLModel, table=True):
    """
    SQLModel table representing a user account.

    Attributes:
        id: Unique identifier (UUID primary key)
        email: User email address (unique, required)
        hashed_password: Bcrypt hashed password
        created_at: Timestamp when user was created
        updated_at: Timestamp when user was last modified
    """

    id: UUID = SQLField(
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
        description="Unique user identifier",
    )

    email: str = SQLField(
        unique=True,
        nullable=False,
        description="User email address",
    )

    hashed_password: str = SQLField(
        nullable=False,
        description="Bcrypt hashed password",
    )

    created_at: datetime = SQLField(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Creation timestamp",
    )

    updated_at: datetime = SQLField(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Last modification timestamp",
    )

    class Config:
        from_attributes = True