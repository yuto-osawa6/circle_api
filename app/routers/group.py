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

@router.post("/groups", response_model=group_schema.GroupCreateResponse)
async def create_group(body: group_schema.GroupCreate,db: AsyncSession = Depends(get_db),token = Depends(get_user)):
    user = await get_user2(db,token)
    return await group_crud.create_group4(db,body,user)

@router.get("/groups/{group_id}",response_model = group_schema.ShowGroup)
async def get_group(group_id: int, db: AsyncSession = Depends(get_db)):
    return await group_crud.get_group_by_id(db,group_id)

@router.get("/users/{user_id}/groups", response_model=group_schema.ReadUserGroup)
# async def read_groups(user_id: int, db: AsyncSession = Depends(get_db),token = Depends(get_user)):
async def read_groups(user_id: int, db: AsyncSession = Depends(get_db)):

    # user = await get_user2(db,token)
    # skip = (page - 1) * limit
    # users = await group_crud.get_groups(db, skip=skip, limit=limit)
    # # return {"users": users}
    # return await group_crud.get_user_groups(db,user_id,user,1,30)
    return await group_crud.get_user_groups(db,user_id,1,30)
