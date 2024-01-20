from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.cruds.user import get_user2

# schema
import app.schemas.group as group_schema
import app.schemas.user as user_schema
import app.schemas.tag as tag_schema

# model
import app.models.group as group_model
import app.models.user as user_model
import app.models.tag as tag_model
import app.models.group_chat as group_chat_model

# traceback
import traceback

from typing import List, Tuple, Optional
from sqlalchemy import select,func
from sqlalchemy.orm import selectinload,load_only,joinedload,subqueryload, relationship, contains_eager
from sqlalchemy.engine import Result
from sqlalchemy.sql import text

import time

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
    
# これ使ってる　上はたぶんつかってない。
async def create_group4(db: AsyncSession, group_create: group_schema.GroupCreate,user):
    print(f"group_create bodyです！:{group_create}")
# async def create_group4(db: AsyncSession, group_create: group_schema.GroupCreate):
    if not group_create.name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Group name is required')
    if group_create.level is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Group level is required')
    try:
        group = group_model.Group(
            name=group_create.name, level=group_create.level, description=group_create.description)
        db.add(group)
        # tagの追加
        # Tagの追加
        for tag_data in group_create.tags:
            existing_tags = await db.execute(select(tag_model.Tag).where(tag_model.Tag.tag_name == tag_data.tag_name))
            # tag = tag_model.Tag(tag_name=tag_data.tag_name)  # ここでtag_nameには適切なデータを入れる
            # check2 scalars().first()あると思うけどエラー出たので、時間ないので。一旦これで。
            existing_tags = existing_tags.scalars().all()
            existing_tag = existing_tags[0] if existing_tags else None

            if existing_tag:
            # If tag already exists, use the existing one
                group.tags.append(existing_tag)
            else:
                # If tag doesn't exist, create a new one
                new_tag = tag_model.Tag(tag_name=tag_data.tag_name)
                db.add(new_tag)
                group.tags.append(new_tag)
            
            # db.add(tag)
            # group.tags.append(tag) 
        # await db.flush()
        print(f"group:{group.id}")
        print(f"group:{vars(group)}")

        db_group_user = group_model.GroupUser(
            group=group, user_id=user.id, authority=0)
            # group=group, user_id=10, authority=0)
        db.add(db_group_user)
        await db.commit()
        await db.refresh(group)
        await db.refresh(db_group_user)
        print(f"group2:{vars(group)}")
        print(f"group2:{group.id}")
        print(f"group2:{vars(group.tags)}")

        # シリアライズ check1 これ無駄にtagを読み込んでる可能性。もっといい方法あるかも。
        group_response = group_schema.GroupCreateResponse(
            id=group.id,
            name=group.name,
            level=group.level,
            description=group.description,
            tags=[tag_schema.TagBase(id=tag.id,tag_name=tag.tag_name) for tag in group.tags],
            # tags=group.tags
        )
        # print(f"レスポンス:{group_response}")
        return group_response
        # return group
    except Exception as e:
        print(f"error:{e}")
        # print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# show group

async def get_group_by_id(db: AsyncSession, group_id: int) -> group_schema.ShowGroup:
    group =await db.query(group_model.Group).filter(group_model.Group.id == group_id).first()
    users = await db.query(user_model.User).join(group_model.GroupUser).filter(group_model.Group.GroupUser.group_id == group_id).all()
    return {"group": group, "users": users}


# get group by user
# async def get_user_groups(db: AsyncSession,user_id:int,user:user_model.User,  page: int = 1,limit: int = 20):
async def get_user_groups(db: AsyncSession,user_id:int,  page: int = 1,limit: int = 20):
    start_time = time.time()
    result = await db.execute(
        select(group_model.Group)
        # .join(group_model.Group.group_chats)
        .join(group_model.Group.users)
        # .join(group_model.Group.tags)
        .filter(user_model.User.id == user_id)
        .offset((page - 1) * limit)
    )
    groups = result.scalars().all()

    # groupsに含まれるGroupのidを取得
    group_ids = [group.id for group in groups]
    print(f"group_ids:{group_ids}")

    # 取得したgroup_idsを元にchatsを取得
    chats_query = (
        select(group_chat_model.GroupChat)
        .options(selectinload(group_chat_model.GroupChat.content))
        .filter(group_chat_model.GroupChat.group_id.in_(group_ids))
        .order_by(group_chat_model.GroupChat.group_id, group_chat_model.GroupChat.id)
        .where(
            func.row_number().over(
                partition_by=group_chat_model.GroupChat.group_id,
                order_by=group_chat_model.GroupChat.id
            ).between(1, 10)
        )
    )
    result_chats = await db.execute(chats_query)
    chats = result_chats.scalars().all()

    print(list(chats))

    # print([chats])
    # return groups
    # start_time = time.time()
    # subquery = (
    #     select(group_chat_model.GroupChat)
    #     .filter(group_chat_model.GroupChat.group_id == group_model.Group.id)
    #     .limit(limit)
    #     .correlate(group_model.Group)
    #     .alias()
    # )
    # result = await db.execute(
    #     # select(group_model.Group,group_chat_model.GroupChat)
    #     select(group_model.Group)
    #     .join(group_model.Group.group_chats)
    #     .join(group_model.Group.users)
    #     .join(group_model.Group.tags)
    #     .outerjoin(subquery)
    #     # .join(subquery)
    #     .filter(user_model.User.id == user_id)
    #     # .options(selectinload(group_model.Group.group_chats))
    #     # .options(
    #     #     contains_eager(group_model.Group.group_chats)
    #     #     .limit(limit)
    #     # )
    #     # .select_from(subquery)
    #     .offset((page - 1) * limit)
    # )
    # groups = result.scalars().all()
    print(groups)
    print(f"akmfkds")
    # # ユーザーが所属する各グループに関連するチャットを取得
    # print(list(group.id for group in groups))
    # group_chat_query = (
    #     select(group_chat_model.GroupChat)
    #     .where(group_chat_model.GroupChat.group_id.in_([group.id for group in groups]))
    # )

    # # チャットを取得
    # group_chats_result = await db.execute(group_chat_query)
    # group_chats = group_chats_result.scalars().all()

    # print([group_chats])
    # print()

    elapsed_time = time.time() - start_time
    print(f"elapsed_time: {elapsed_time}")
    # return {"groups": groups,"group_chats":group_chats}
    return {"groups": groups,"group_chats" : chats}



