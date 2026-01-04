"""
MCP Tools for Phase III AI Chatbot.

This module provides MCP-compatible tools for task CRUD operations.
Each tool enforces user_id isolation for data security.

Tools:
- add_task: Create a new task
- list_tasks: List user's tasks (optionally filtered by status)
- complete_task: Mark a task as complete
- update_task: Update task title or due date
- delete_task: Delete a task
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models import Task

logger = logging.getLogger(__name__)


def _serialize_task(task: Task) -> Dict[str, Any]:
    """Serialize a Task model to a dictionary for JSON response."""
    return {
        "id": str(task.id),
        "user_id": str(task.user_id),
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
    }


async def add_task(
    db: AsyncSession,
    user_id: UUID,
    title: str,
    due_date: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a new task for the authenticated user.

    Args:
        db: Database session
        user_id: ID of the owning user (from JWT)
        title: Task title (required)
        due_date: Optional due date in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)

    Returns:
        Dict with success status, task_id, and task details

    Raises:
        ValueError: If title is empty
    """
    # Validate title
    if not title or not title.strip():
        raise ValueError("Task title is required")

    # Parse due date if provided
    parsed_due_date = None
    if due_date:
        try:
            # Try ISO format first
            parsed_due_date = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
        except ValueError:
            try:
                # Try date-only format
                parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Invalid due_date format: {due_date}. Use YYYY-MM-DD or ISO format")

    # Create task
    task = Task(
        user_id=user_id,
        title=title.strip(),
        due_date=parsed_due_date,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)

    logger.info(f"Task created: {task.id} for user {user_id}")

    return {
        "success": True,
        "task_id": str(task.id),
        "task": _serialize_task(task),
    }


async def list_tasks(
    db: AsyncSession,
    user_id: UUID,
    status: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    List tasks for the authenticated user.

    Args:
        db: Database session
        user_id: ID of the owning user (from JWT)
        status: Optional filter - "pending" or "complete"

    Returns:
        List of task dictionaries with id, title, due_date, status, etc.
    """
    # Build query with user isolation
    query = select(Task).where(Task.user_id == user_id)

    # Apply status filter if provided
    if status == "pending":
        query = query.where(Task.completed == False)
    elif status == "complete":
        query = query.where(Task.completed == True)

    # Order by creation date (newest first)
    query = query.order_by(Task.created_at.desc())

    result = await db.execute(query)
    tasks = result.scalars().all()

    logger.info(f"Listed {len(tasks)} tasks for user {user_id}")

    return [_serialize_task(task) for task in tasks]


async def complete_task(
    db: AsyncSession,
    user_id: UUID,
    task_id: str,
) -> Dict[str, Any]:
    """
    Mark a task as complete.

    Args:
        db: Database session
        user_id: ID of the owning user (from JWT)
        task_id: UUID of the task to complete

    Returns:
        Dict with success status and updated task details

    Raises:
        ValueError: If task_id is invalid or task not found
    """
    # Parse task_id
    try:
        parsed_task_id = UUID(task_id)
    except ValueError:
        raise ValueError(f"Invalid task_id format: {task_id}")

    # Find task with user isolation
    result = await db.execute(
        select(Task).where(Task.id == parsed_task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if task is None:
        raise ValueError("Task not found or access denied")

    # Update task
    task.completed = True
    await db.commit()
    await db.refresh(task)

    logger.info(f"Task completed: {task.id} for user {user_id}")

    return {
        "success": True,
        "task_id": str(task.id),
        "task": _serialize_task(task),
    }


async def update_task(
    db: AsyncSession,
    user_id: UUID,
    task_id: str,
    title: Optional[str] = None,
    due_date: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Update a task's title or due date.

    Args:
        db: Database session
        user_id: ID of the owning user (from JWT)
        task_id: UUID of the task to update
        title: Optional new title
        due_date: Optional new due date in ISO format

    Returns:
        Dict with success status and updated task details

    Raises:
        ValueError: If task_id is invalid, task not found, or title is empty
    """
    # Parse task_id
    try:
        parsed_task_id = UUID(task_id)
    except ValueError:
        raise ValueError(f"Invalid task_id format: {task_id}")

    # Find task with user isolation
    result = await db.execute(
        select(Task).where(Task.id == parsed_task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if task is None:
        raise ValueError("Task not found or access denied")

    # Update title if provided
    if title is not None:
        if not title.strip():
            raise ValueError("Task title cannot be empty")
        task.title = title.strip()

    # Update due_date if provided
    if due_date is not None:
        try:
            task.due_date = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
        except ValueError:
            try:
                task.due_date = datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Invalid due_date format: {due_date}. Use YYYY-MM-DD or ISO format")

    await db.commit()
    await db.refresh(task)

    logger.info(f"Task updated: {task.id} for user {user_id}")

    return {
        "success": True,
        "task_id": str(task.id),
        "task": _serialize_task(task),
    }


async def delete_task(
    db: AsyncSession,
    user_id: UUID,
    task_id: Optional[str] = None,
    title: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Delete a task by ID or title.

    Args:
        db: Database session
        user_id: ID of the owning user (from JWT)
        task_id: UUID of the task to delete (optional)
        title: Title of the task to delete (optional)

    Returns:
        Dict with success status and deleted task info

    Raises:
        ValueError: If neither task_id nor title provided, or task not found
    """
    if not task_id and not title:
        raise ValueError("Either task_id or title must be provided")

    # Find task with user isolation
    if task_id:
        try:
            parsed_task_id = UUID(task_id)
            query = select(Task).where(Task.id == parsed_task_id, Task.user_id == user_id)
        except ValueError:
            raise ValueError(f"Invalid task_id format: {task_id}")
    else:
        # Search by title
        query = select(Task).where(Task.title.ilike(f"%{title}%"), Task.user_id == user_id)

    result = await db.execute(query)
    task = result.scalar_one_or_none()

    if task is None:
        raise ValueError("Task not found or access denied")

    # Store task info for response before deletion
    deleted_task_info = {
        "task_id": str(task.id),
        "title": task.title
    }

    # Delete task
    await db.delete(task)
    await db.commit()

    logger.info(f"Task deleted: {deleted_task_info['task_id']} for user {user_id}")

    return {
        "success": True,
        "task_id": deleted_task_info["task_id"],
        "status": "deleted",
        "title": deleted_task_info["title"]
    }
