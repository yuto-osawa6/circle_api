# from typing import List
import app.schemas.group as group_schema

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import app.cruds.group as group_crud
from app.cruds.user import get_user
# from app.cruds.user import get_user_by_token
import app.schemas.user as user_schema
from app.cruds.user import get_user2

import app.schemas.group as group_schema
# import app.schemas.group as group_schema
# import app.cruds.user as user_crud
from app.db import get_db

router = APIRouter()

@router.get("/hello")
def hello():
    return{"a":"hello"}

# @router.post("/groups", response_model=group_schema.GroupCreate)
# async def create_group(body: group_schema.GroupCreate,db: AsyncSession = Depends(get_db),token = Depends(get_user)):
#     # user = await get_user2(db,token)
#     user:user_schema.User = await get_user2(await db.connection(), token)
#     return await group_crud.create_group2(db,body,user)

# @router.post("/groups", response_model=group_schema.GroupCreate)
# async def create_group(body: group_schema.GroupCreate,db: AsyncSession = Depends(get_db)):
#     # user = await get_user2(db,token)
#     # user:user_schema.User = await get_user2(await db.connection(), token)
#     return await group_crud.create_group3(db,body)

# した3
# @router.post("/groups", response_model=group_schema.GroupCreate)
# async def create_group(body: group_schema.GroupCreate,db: AsyncSession = Depends(get_db)):
#     # user = await get_user2(await db.connection(),token)
#     # user:user_schema.User = await get_user2(await db.connection(), token)
#     return await group_crud.create_group3(db,body)

@router.post("/groups", response_model=group_schema.GroupCreate)
async def create_group(body: group_schema.GroupCreate,db: AsyncSession = Depends(get_db),token = Depends(get_user)):
    # user = await get_user2(await db.connection(),token)
    user = await get_user2(db,token)

    # print(f"user:{user}")
    # print(user.id)
    # user:user_schema.User = await get_user2(await db.connection(), token)
    return await group_crud.create_group4(db,body,user)

# 消しちゃダメ
# @router.post("/groups", response_model=group_schema.GroupCreate)
# async def create_group(body: group_schema.GroupCreate,db: AsyncSession = Depends(get_db),token = Depends(get_user)):
#     # user = await get_user_by_token(db,body)
#     return await group_crud.create_group(db,body,token)

# @router.post("/tasks", response_model=task_schema.TaskCreateResponse)
# async def create_task(
#     task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)
# ):
#     return await task_crud.create_task(db, task_body)