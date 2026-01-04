"""
Task API routes - DEMO MODE: Auth bypassed
"""

import logging
from typing import Annotated
from fastapi import APIRouter, HTTPException, Request, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID, uuid4  # 👈 uuid4 add kiya for dummy user_id
from ..db import get_db
from ..models import Task, TaskCreate, TaskUpdate, TaskResponse, TaskListResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.get("", response_model=TaskListResponse)
async def list_tasks(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TaskListResponse:
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
    if not task_data.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")
    
    # 🔥 FIX: Dummy fixed UUID (ya random) daal do taaki NOT NULL error na aaye
    dummy_user_id = uuid4()  # Har task ke liye unique dummy user
    # Ya fixed ek UUID: UUID("00000000-0000-0000-0000-000000000001")

    task = Task(
        user_id=dummy_user_id,  # 👈 Ye MUST hai, None mat daalo
        title=task_data.title.strip(),
        description=task_data.description.strip() if task_data.description else None,
        completed=False,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    logger.info(f"Task created in demo mode: {task.id}")
    return TaskResponse.from_orm(task)

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]) -> TaskResponse:
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse.from_orm(task)

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID, task_data: TaskUpdate, db: Annotated[AsyncSession, Depends(get_db)]
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
async def delete_task(task_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]) -> None:
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.delete(task)
    await db.commit()

@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_complete(
    task_id: UUID, request: Request, db: Annotated[AsyncSession, Depends(get_db)]
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
