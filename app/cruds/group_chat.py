from typing import Optional
import asyncio
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

# import firebase_admin
# from firebase_admin import credentials
from firebase_admin import messaging

redis_client = redis.Redis(host='redis', port=6379)
# import redis

#  post create_group_chat_content

async def send_fcm_notification(device_token, title, body):
    print(title,device_token,body)
    # FCM通知メッセージの作成
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        token=device_token,
    )

    # FCM通知の送信
    response = messaging.send(message)
    print('FCM Notification sent successfully:', response)

async def load_users(db: AsyncSession, group_id: int) -> List[user_model.User]:
    query = select(user_model.User).join(user_model.User.groups).where(group_model.Group.id == group_id)
    result = await db.execute(query)
    users = result.scalars().all()
    return users

# check-1 errorがでたときをfrontに送ってない、
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

            # # 中間テーブルを経由して関連するユーザーを取得するクエリを実行する
            # users_query = select(user_model.User).join(user_model.User.groups).where(group_model.Group.id == content.group_id)
            # # users_task = asyncio.create_task(db.execute(users_query))
            # users_result = await db.execute(users_query)
            # # users = users_result.scalars().all()
            # # users = users_result.all()
            # users = [user[0] for user in users_result.all()]

            
            # # ユーザーデータの遅延ロード
            # users = await load_users(db, content.group_id)
            # print(users)
            # print("users")
            # print(users[0].id)

            # ユーザーデータの遅延ロード
            # await asyncio.gather(*[db.refresh(user) for user in users])


        await db.commit()
        await db.refresh(group_chat_content)
            # await db.refresh(group_chat, options=[selectinload(group_chat_model.GroupChat.content)])
        await db.refresh(group_chat)

        # async with db.begin():
        #     # 中間テーブルを経由して関連するユーザーを取得するクエリを実行する
        #     users = db.execute(
        #         select(user_model.User)
        #         .join(user_model.User.groups)
        #         .where(group_model.Group.id == content.group_id)
        #     )
        #     print(users)
        #     print("users!!グループに属するユーザー情報")


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

        # 通知の処理を遅延させる
        # async with db.begin():
            # ユーザーデータの遅延ロード
        users = await load_users(db, content.group_id)
        print(users)
        print("users")
        # print(users.id)
            # print(users)
        for user in users:
            try:
                print(user)
                print(vars(user))
                print(user.device_token)
                await send_fcm_notification(user.device_token, 
                    "新しいメッセージが届きました",
                    "新しいメッセージがあります。チャットを確認してください。"
                )
            except Exception as e:
                print(f"Error sending FCM notification for user {user.id}: {e}")
            continue
        # users = await users_task
        # print(users.all())
        print("users!!グループに属するユーザー情報")


        return "message 1"
    except Exception as e:
        print(e)
        print("jaijfeioajioea")
    # finally:
    #     await db.close()

# Get group chat グループチャット一覧の取得。


# get group by user
async def get_group_chats(db: AsyncSession, group_id: int,  page: int = 1, limit: int = 30):
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
