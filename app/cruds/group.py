from typing import Optional
from fastapi import FastAPI, Depends,HTTPException, status
from app.routers import task
import app.schemas.group as group_schema
import app.models.group as group_model

from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db

async def create_group(db: AsyncSession,group_create: group_schema.GroupCreate,token):
    print(token)
    # try:
    print(group_create)
    print(group_create.dict())
    if not group_create.name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Group name is required')
    group = group_model.Group(**group_create.dict())
    db.add(group)
    await db.commit()
    await db.refresh(group)
    return group
    # except Exception as e:
    #     db.rollback()
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# async def create_task(
#     db: AsyncSession, task_create: task_schema.TaskCreate
# ) -> task_model.Task:
#     task = task_model.Task(**task_create.dict())
#     db.add(task)
#     await db.commit()
#     await db.refresh(task)
#     return task