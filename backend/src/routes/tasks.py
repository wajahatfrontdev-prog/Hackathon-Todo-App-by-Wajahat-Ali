"""
Task API routes for the Todo Web Application.
This module provides all task CRUD endpoints:
- GET /api/tasks - List all user's tasks
- POST /api/tasks - Create a new task
- GET /api/tasks/{task_id} - Get a single task
- PUT /api/tasks/{task_id} - Update a task
- DELETE /api/tasks/{task_id} - Delete a task
- PATCH /api/tasks/{task_id}/complete - Toggle task completion

🔥 TEMPORARY FOR HACKATHON DEMO: Authentication bypassed (get_current_user removed)
   → All tasks are now publicly accessible (no JWT required)
   → Assuming single-user demo or all tasks shown to everyone for judging
"""

import logging
from typing import Annotated
from fastapi import APIRouter, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from ..db import get_db
from ..models import Task, TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
# from ..dependencies.auth import get_current_user  # ← COMMENTED OUT FOR DEMO

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

# 🔥 AUTH BYPASSED: Removed current_user_id dependency from all routes

@router.get("", response_model=TaskListResponse)
async def list_tasks(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TaskListResponse:
    """
    TEMP DEMO: List ALL tasks (no user filter - shows everyone's tasks)
    """
    result = await db.execute(select(Task).order_by(Task.created_at.desc()))
    tasks = result.scalars().all()
    return TaskListResponse(
        tasks=[TaskResponse.from_orm(task) for task in tasks],
        total=len(tasks),
    )

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TaskResponse:
    """
    TEMP DEMO: Create task without user association (user_id = None or fixed demo user)
    """
    if not task_data.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title is required",
        )
    
    # 🔥 For demo: Set a fixed dummy user_id or leave as None if your model allows
    task = Task(
        user_id=None,  # Ya ek fixed UUID rakh do jaise UUID("00000000-0000-0000-0000-000000000001")
        title=task_data.title.strip(),
        description=task_data.description.strip() if task_data.description else None,
        completed=False,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    logger.info(f"Task created (demo mode): {task.id}")
    return TaskResponse.from_orm(task)

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TaskResponse:
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse.from_orm(task)

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TaskResponse:
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task_data.title is not None:
        if not task_data.title.strip():
            raise HTTPException(status_code=400, detail="Title is required")
        task.title = task_data.title.strip()
    if task_data.description is not None:
        task.description = task_data.description.strip() if task_data.description else None
    
    await db.commit()
    await db.refresh(task)
    return TaskResponse.from_orm(task)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.delete(task)
    await db.commit()

@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_complete(
    task_id: UUID,
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TaskResponse:
    body = await request.json()
    completed = body.get("completed")
    if completed is None or not isinstance(completed, bool):
        raise HTTPException(status_code=400, detail="'completed' field is required and must be a boolean")
    
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.completed = completed
    await db.commit()
    await db.refresh(task)
    return TaskResponse.from_orm(task)
