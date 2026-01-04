"""
Task API routes for the Todo Web Application.

This module provides all task CRUD endpoints:
- GET /api/tasks - List all user's tasks
- POST /api/tasks - Create a new task
- GET /api/tasks/{task_id} - Get a single task
- PUT /api/tasks/{task_id} - Update a task
- DELETE /api/tasks/{task_id} - Delete a task
- PATCH /api/tasks/{task_id}/complete - Toggle task completion

All endpoints require JWT authentication via get_current_user dependency.
All queries are filtered by current_user.id for data isolation.
"""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from ..db import get_db
from ..models import Task, TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from ..dependencies.auth import get_current_user

# Configure logging
logger = logging.getLogger(__name__)

# Create router with /api/tasks prefix
router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    current_user_id: Annotated[UUID, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TaskListResponse:
    """
    List all tasks for the authenticated user.

    Returns a list of all tasks belonging to the current user,
    ordered by creation date (newest first).

    Args:
        current_user_id: UUID from JWT token (injected by get_current_user)
        db: Database session (injected by get_db)

    Returns:
        TaskListResponse: List of tasks with total count

    Response:
        - 200: Success - returns list of tasks
        - 401: Unauthorized - missing or invalid JWT token
    """
    result = await db.execute(
        select(Task)
        .where(Task.user_id == current_user_id)
        .order_by(Task.created_at.desc())
    )
    tasks = result.scalars().all()
    return TaskListResponse(
        tasks=[TaskResponse.from_orm(task) for task in tasks],
        total=len(tasks),
    )


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user_id: Annotated[UUID, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TaskResponse:
    """
    Create a new task for the authenticated user.

    The task is automatically associated with the authenticated user's ID.

    Args:
        task_data: Task creation data (title required, description optional)
        current_user_id: UUID from JWT token
        db: Database session

    Returns:
        TaskResponse: The created task

    Raises:
        400: Bad Request - title is empty or validation fails
        401: Unauthorized - missing or invalid JWT token
    """
    # Validate title is not empty after stripping whitespace
    if not task_data.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title is required",
        )

    # Create new task associated with the current user
    task = Task(
        user_id=current_user_id,
        title=task_data.title.strip(),
        description=task_data.description.strip() if task_data.description else None,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)

    logger.info(f"Task created: {task.id} for user {current_user_id}")
    return TaskResponse.from_orm(task)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    current_user_id: Annotated[UUID, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TaskResponse:
    """
    Get a single task by ID.

    Returns a specific task only if it belongs to the authenticated user.

    Args:
        task_id: UUID of the task to retrieve
        current_user_id: UUID from JWT token
        db: Database session

    Returns:
        TaskResponse: The requested task

    Raises:
        401: Unauthorized - missing or invalid JWT token
        403: Forbidden - task belongs to another user
        404: Not Found - task does not exist
    """
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    if task.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task",
        )

    return TaskResponse.from_orm(task)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    current_user_id: Annotated[UUID, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TaskResponse:
    """
    Update an existing task.

    Updates only the fields that are provided in the request body.
    Only the task owner can update their tasks.

    Args:
        task_id: UUID of the task to update
        task_data: Update data (fields are optional)
        current_user_id: UUID from JWT token
        db: Database session

    Returns:
        TaskResponse: The updated task

    Raises:
        400: Bad Request - title is empty
        401: Unauthorized - missing or invalid JWT token
        403: Forbidden - task belongs to another user
        404: Not Found - task does not exist
    """
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    if task.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task",
        )

    # Update fields if provided
    if task_data.title is not None:
        if not task_data.title.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title is required",
            )
        task.title = task_data.title.strip()

    if task_data.description is not None:
        task.description = task_data.description.strip() if task_data.description else None

    await db.commit()
    await db.refresh(task)

    logger.info(f"Task updated: {task_id}")
    return TaskResponse.from_orm(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    current_user_id: Annotated[UUID, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    """
    Delete a task.

    Only the task owner can delete their tasks.

    Args:
        task_id: UUID of the task to delete
        current_user_id: UUID from JWT token
        db: Database session

    Raises:
        401: Unauthorized - missing or invalid JWT token
        403: Forbidden - task belongs to another user
        404: Not Found - task does not exist
    """
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    if task.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task",
        )

    await db.delete(task)
    await db.commit()

    logger.info(f"Task deleted: {task_id}")


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_complete(
    task_id: UUID,
    request: Request,
    current_user_id: Annotated[UUID, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TaskResponse:
    """
    Toggle the completion status of a task.

    Sets the task's completed field to the value provided in the request body.
    Only the task owner can toggle their tasks.

    Args:
        task_id: UUID of the task to toggle
        request: HTTP request containing JSON body with 'completed' field
        current_user_id: UUID from JWT token
        db: Database session

    Request Body:
        {
            "completed": true  # or false
        }

    Returns:
        TaskResponse: The updated task

    Raises:
        400: Bad Request - 'completed' field is missing or not a boolean
        401: Unauthorized - missing or invalid JWT token
        403: Forbidden - task belongs to another user
        404: Not Found - task does not exist
    """
    body = await request.json()
    completed = body.get("completed")

    if completed is None or not isinstance(completed, bool):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="'completed' field is required and must be a boolean",
        )

    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    if task.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task",
        )

    task.completed = completed
    await db.commit()
    await db.refresh(task)

    logger.info(f"Task completion toggled: {task_id} -> {completed}")
    return TaskResponse.from_orm(task)
