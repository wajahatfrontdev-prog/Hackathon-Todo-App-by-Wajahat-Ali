"""
Pydantic schemas for error responses.
"""

from pydantic import Field
from sqlmodel import SQLModel


class ErrorResponse(SQLModel):
    """
    Pydantic schema for error responses.

    Attributes:
        detail: Human-readable error message
    """

    detail: str = Field(..., description="Error message")