"""
SQLModel database models and Pydantic schemas for Task entities.

This module defines:
- Task: SQLModel table for storing todo items
- TaskCreate: Schema for creating new tasks
- TaskUpdate: Schema for updating existing tasks
- TaskResponse: Schema for task API responses
- TaskListResponse: Schema for task list responses
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field
from sqlmodel import Field as SQLField, SQLModel


class Task(SQLModel, table=True):
    """
    SQLModel table representing a todo task owned by a user.

    Attributes:
        id: Unique identifier (UUID primary key)
        user_id: Foreign key to the owning user (managed by Better Auth)
        title: Task title (required, 1-500 characters)
        description: Optional task details (max 5000 characters)
        completed: Completion status (default False)
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last modified

    Relationships:
        user: Many-to-one relationship with User (for FK reference)

    Note:
        - The User table is managed by Better Auth on the frontend
        - user_id is a required foreign key for data isolation
        - All queries must filter by user_id for user-specific data
    """

    id: UUID = SQLField(
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
        description="Unique task identifier",
    )

    user_id: UUID = SQLField(
        nullable=False,
        description="Foreign key to the owning user",
    )

    title: str = SQLField(
        min_length=1,
        max_length=500,
        nullable=False,
        description="Task title (required, 1-500 characters)",
    )

    description: Optional[str] = SQLField(
        default=None,
        max_length=5000,
        nullable=True,
        description="Optional task details (max 5000 characters)",
    )

    completed: bool = SQLField(
        default=False,
        nullable=False,
        description="Completion status",
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


class TaskCreate(SQLModel):
    """
    Pydantic schema for creating a new task.

    Attributes:
        title: Task title (required, 1-500 characters)
        description: Optional task details (max 5000 characters)

    Validation:
        - Title must be non-empty after stripping whitespace
        - Description is optional and can be None or empty string
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Task title (required, 1-500 characters)",
        examples=["Buy groceries"],
    )

    description: Optional[str] = Field(
        default=None,
        max_length=5000,
        description="Optional task details",
        examples=["Milk, eggs, bread"],
    )


class TaskUpdate(SQLModel):
    """
    Pydantic schema for updating an existing task.

    All fields are optional - only provided fields will be updated.

    Attributes:
        title: Updated task title (1-500 characters)
        description: Updated task details (max 5000 characters)
        completed: Updated completion status
    """

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=500,
        description="Task title (1-500 characters, optional for updates)",
    )

    description: Optional[str] = Field(
        default=None,
        max_length=5000,
        description="Task details (optional for updates)",
    )

    completed: Optional[bool] = Field(
        default=None,
        description="Completion status (optional for updates)",
    )


class TaskResponse(SQLModel):
    """
    Pydantic schema for task API responses.

    This schema is used for serializing Task data in API responses.
    All datetime fields are converted to ISO 8601 string format.

    Attributes:
        id: Task UUID as string
        user_id: Owning user UUID as string
        title: Task title
        description: Task details or null
        completed: Completion status
        created_at: Creation timestamp as ISO string
        updated_at: Modification timestamp as ISO string
    """

    id: str = Field(..., description="Task UUID")
    user_id: str = Field(..., description="Owning user UUID")
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(default=None, description="Task details")
    completed: bool = Field(..., description="Completion status")
    created_at: str = Field(..., description="Creation timestamp (ISO 8601)")
    updated_at: str = Field(..., description="Modification timestamp (ISO 8601)")

    @classmethod
    def from_orm(cls, task: Task) -> "TaskResponse":
        """
        Convert a Task SQLModel instance to TaskResponse.

        Args:
            task: SQLModel Task instance

        Returns:
            TaskResponse instance with string UUIDs and formatted timestamps
        """
        return cls(
            id=str(task.id),
            user_id=str(task.user_id),
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at.isoformat(),
            updated_at=task.updated_at.isoformat(),
        )


class TaskListResponse(SQLModel):
    """
    Pydantic schema for the task list API response.

    Attributes:
        tasks: List of TaskResponse objects
        total: Total number of tasks in the list
    """

    tasks: list[TaskResponse] = Field(default_factory=list, description="List of tasks")
    total: int = Field(..., description="Total number of tasks")