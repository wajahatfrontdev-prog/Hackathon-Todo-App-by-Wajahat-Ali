"""
Models package for the Todo Web Application.

This package exports:
- User: SQLModel for user accounts
- Task: SQLModel for todo tasks
- TaskCreate: Schema for creating tasks
- TaskUpdate: Schema for updating tasks
- TaskResponse: Schema for task responses
- TaskListResponse: Schema for task list responses
- Conversation: SQLModel for chat conversations
- Message: SQLModel for chat messages
- MessageRole: Enum for message roles (user/assistant)
- ErrorResponse: Schema for error responses
"""

from .user import User
from .task import Task, TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from .chat import Conversation, Message, MessageRole
from .error import ErrorResponse

__all__ = [
    "User",
    "Task",
    "TaskCreate",
    "TaskUpdate",
    "TaskResponse",
    "TaskListResponse",
    "Conversation",
    "Message",
    "MessageRole",
    "ErrorResponse",
]