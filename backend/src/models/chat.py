"""
Database models for Phase III AI Chatbot.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, Relationship


class MessageRole(str, Enum):
    """Message role enumeration."""
    USER = "user"
    ASSISTANT = "assistant"


class Conversation(SQLModel, table=True):
    """Conversation model for chat sessions."""
    
    __tablename__ = "conversations"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(index=True)  # Remove foreign key constraint
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    messages: list["Message"] = Relationship(back_populates="conversation")


class Message(SQLModel, table=True):
    """Message model for chat history."""
    
    __tablename__ = "messages"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True)
    role: MessageRole = Field(index=True)
    content: str = Field(max_length=10000)
    tool_calls: Optional[str] = Field(default=None)  # JSON string
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")