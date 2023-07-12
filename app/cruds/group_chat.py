from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.cruds.user import get_user2

# schema
import app.schemas.group as group_schema
import app.schemas.group_chat as group_chat_schema

import app.schemas.user as user_schema
# model
import app.models.group as group_model
import app.models.user as user_model

import app.models.group_chat as group_chat_model


# traceback
import traceback

from typing import List, Tuple, Optional
from sqlalchemy import select,desc
from sqlalchemy.orm import selectinload,joinedload
from sqlalchemy.engine import Result

import redis
import json

redis_client = redis.Redis(host='redis', port=6379)
# import redis

#  post create_group_chat_content


async def create_group_chat_content(db: AsyncSession, content: group_chat_schema.GroupChatContentCreate):
    try:
        async with db.begin():
            group_chat = group_chat_model.GroupChat(
                group_id=content.group_id, user_id=content.user_id)
            db.add(group_chat)
            # await db.flush()
            print(f'group_chat:{vars(group_chat)}')

            group_chat_content = group_chat_model.GroupChatContent(
                group_chat=group_chat,
                content_type=content.content_type,
                s3_object_key=content.s3_object_key,
                text_content=content.text_content
            )
            db.add(group_chat_content)
        await db.commit()

        await db.refresh(group_chat_content)
        # await db.refresh(group_chat, options=[selectinload(group_chat_model.GroupChat.content)])
        await db.refresh(group_chat)

        room = f"group_chanel{group_chat.group_id}"
        print(f"rooooooooom{group_chat_content}")
        redis_client.publish(room, json.dumps({
        "id": group_chat.id,
        "group_id": group_chat.group_id,
        "user_id": group_chat.user_id,
        "content": {
            "group_chat_id": group_chat_content.group_chat_id,
            "content_type": group_chat_content.content_type,
            "text_content": group_chat_content.text_content,
            "s3_object_key": group_chat_content.s3_object_key,
            "id": group_chat_content.id
        }
        }).encode('utf-8'))
        return "message 1"
    except:
        print("jaijfeioajioea")
    # finally:
    #     await db.close()

# Get group chat グループチャット一覧の取得。


# get group by user
async def get_group_chats(db: AsyncSession, group_id: int,  page: int = 1, limit: int = 10):
    print(f"page:{page}")
    print(f"limit{limit}")
    # ユーザーの存在確認
    # user1 = await db.query(user_model.User).filter(user_model.id == user_id).first_async()
    # async with db.begin():
    result: Result = await db.execute(
        select(group_chat_model.GroupChat).options(joinedload(
            group_chat_model.GroupChat.content))
            .filter(group_chat_model.GroupChat.group_id == group_id)
            .order_by(desc(group_chat_model.GroupChat.created_at))
            .offset((page - 1) * limit)
            .limit(limit)
    )
    print(result)
    group_chat: List[group_chat_model.GroupChat] = result.scalars().all()

    print(f"group:{group_chat}")
    print(len(group_chat))
    return group_chat
    # print(f"user:{user[0].id}")
    # print(user[0].groups)
    # print(vars(user[0].groups[0]))
    # print(user[0].groups[0].id)

    # # ページ番号から取得するグループの先頭インデックスを計算
    # start_index = (page - 1) * limit
    # # ユーザーが所属するグループを取得
    # groups = user[0].groups[start_index : start_index + limit]
    # return {"groups":groups}
