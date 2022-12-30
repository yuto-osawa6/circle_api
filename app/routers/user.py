from typing import List
# from fastapi import APIRouter
import app.schemas.task as task_schema

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import app.cruds.task as task_crud
import app.cruds.user as user_crud
from app.db import get_db

router = APIRouter()

# @router.get("/tasks", response_model=List[task_schema.Task])
# async def list_tasks():
#     return [task_schema.Task(id=1, title="1つ目のTODOタスク")]
# @router.get("/tasks")
# async def list_tasks(db: AsyncSession = Depends(get_db)):
#     return await task_crud.get_tasks_with_done(db)

# @router.post("/tasks", response_model=task_schema.TaskCreateResponse)
# async def create_task(
#     task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)
# ):
#     return await task_crud.create_task(db, task_body)

# @router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
# async def update_task(
#     task_id: int, task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)
# ):
#     task = await task_crud.get_task(db, task_id=task_id)
#     if task is None:
#         raise HTTPException(status_code=404, detail="Task not found")

#     return await task_crud.update_task(db, task_body, original=task)

@router.get("/users")
async def list_tasks(db: AsyncSession = Depends(get_db)):
    return await task_crud.get_tasks_with_done(db)

@router.get("/users")
async def list_tasks(db: AsyncSession = Depends(get_db)):
    return await user_crud.get_or_create_user(db)