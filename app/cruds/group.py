from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from app.routers import task
import app.schemas.group as group_schema
import app.models.group as group_model

import app.schemas.user as user_schema

from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.cruds.user import get_user2

# traceback
import traceback

# async def create_group(db: AsyncSession,group_create: group_schema.GroupCreate,token):
#     # user = await get_user2(db,token)
#     print(token)
#     # print(user.id)
#     print("user")
#     print(group_create)
#     print(group_create.dict())
#     print(group_create.level)
#     if not group_create.name:
#       print(group_create.name)
#       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Group name is required')
#     if group_create.level is None:
#       print(group_create.level)
#       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Group level is required')
#     try:
#       group = group_model.Group(**group_create.dict())
#       db.add(group)
#       # group.users.append(user)
#       await db.commit()
#       await db.refresh(group)
#       db_group_user = group_model.GroupUser(group_id=group.id, user_id=10,authority=0)
#       db.add(db_group_user)
#       await db.commit()
#       await db.refresh(db_group_user)
#         # return group
#       return group
#     except Exception as e:
#         print(f"error:{e}")
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# async def create_task(
#     db: AsyncSession, task_create: task_schema.TaskCreate
# ) -> task_model.Task:
#     task = task_model.Task(**task_create.dict())
#     db.add(task)
#     await db.commit()
#     await db.refresh(task)
#     return task


async def create_group(db: AsyncSession, group_create: group_schema.GroupCreate, token):
    user = await get_user2(await db.connection(), token)
    if not group_create.name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Group name is required')
    if group_create.level is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Group level is required')
    try:
        group = group_model.Group(**group_create.dict())
        db.add(group)
        await db.commit()
        await db.refresh(group)

        # 中間テーブルにグループとユーザーを追加
        db_group_user = group_model.GroupUser(
            group_id=group.id, user_id=user.id, authority=0)
        db.add(db_group_user)
        await db.commit()
        await db.refresh(db_group_user)

        return group
    except Exception as e:
        print(f"error:{e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def create_group2(db: AsyncSession, group_create: group_schema.GroupCreate):
    # user = await get_user2(await db.connection(), token)
    if not group_create.name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Group name is required')
    if group_create.level is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Group level is required')
    try:
        # group = group_model.Group(**group_create.dict())
        group = group_model.Group(
            name=group_create.name, level=group_create.level)
        db.add(group)
        await db.commit()
        await db.refresh(group)

        print(group)
        print(group.id)

        # 中間テーブルにグループとユーザーを追加
        # if group.id is not None:
        # db_group_user = group_model.GroupUser(group=group, user_id=user.id, authority=0)
        db_group_user = group_model.GroupUser(
            group_id=group.id, user_id=10, authority=0)
        db.add(db_group_user)
        await db.commit()
        await db.refresh(db_group_user)

        return group
    except Exception as e:
        print(f"error:{e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# 試し
# async def create_group3(db: AsyncSession, group_create: group_schema.GroupCreate):
#     if not group_create.name:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Group name is required')
#     if group_create.level is None:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Group level is required')
#     try:
#         group = group_model.Group(**group_create.dict())
#         # group = group_model.Group(name=group_create.name, level=group_create.level)
#         db.add(group)
#         await db.commit()
#         await db.refresh(group)

#         print(group)
#         print(group.id)

#         # 中間テーブルにグループとユーザーを追加
#         # if group.id is not None:
#         # db_group_user = group_model.GroupUser(group=group, user_id=user.id, authority=0)
#         db_group_user = group_model.GroupUser(group_id=group.id, user_id=10, authority=0)
#         db.add(db_group_user)
#         await db.commit()
#         await db.refresh(db_group_user)

#         return group
#     except Exception as e:
#         print(f"error:{e}")
#         print(traceback.format_exc())
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def create_group3(db: AsyncSession, group_create: group_schema.GroupCreate):
    if not group_create.name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Group name is required')
    if group_create.level is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Group level is required')
    try:
        group = group_model.Group(
            name=group_create.name, level=group_create.level)
        db.add(group)
        print(f"group:{group.id}")
        print(f"group:{group}")


        user_id = 10
        db_group_user = group_model.GroupUser(
            group=group, user_id=user_id, authority=0)
        db.add(db_group_user)
        await db.commit()
        await db.refresh(group)
        await db.refresh(db_group_user)

        # async with db.begin():
        #     group = group_model.Group(
        #         name=group_create.name, level=group_create.level)
        #     db.add(group)
        #     print(f"group:{group.id}")
        #     print(f"group:{group}")

        #     await db.flush()

        #     user_id = 10
        #     db_group_user = group_model.GroupUser(
        #         group=group, user_id=user_id, authority=0)
        #     db.add(db_group_user)

        #     await db.flush()
        #     await db.refresh(group)
            # await db.refresh(db_group_user)
        return group
    except Exception as e:
        print(f"error:{e}")
        # print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
async def create_group4(db: AsyncSession, group_create: group_schema.GroupCreate,user):
    if not group_create.name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Group name is required')
    if group_create.level is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Group level is required')
    try:
        group = group_model.Group(
            name=group_create.name, level=group_create.level)
        db.add(group)
        # await db.flush()
        print(f"group:{group.id}")
        print(f"group:{group}")

        db_group_user = group_model.GroupUser(
            group=group, user_id=user.id, authority=0)
        db.add(db_group_user)
        await db.commit()
        await db.refresh(group)
        await db.refresh(db_group_user)
        return group
    except Exception as e:
        print(f"error:{e}")
        # print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# show group


