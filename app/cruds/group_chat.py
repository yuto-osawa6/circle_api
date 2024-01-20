from typing import Optional
import asyncio
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, desc
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
import app.cruds.user as user_crud


# traceback
import traceback

from typing import List, Tuple, Optional
from sqlalchemy import select,desc
from sqlalchemy.orm import selectinload,joinedload,subqueryload
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
    # APNs用のpayloadを設定
    # apns_payload = messaging.APNSPayload(
    #     aps=messaging.Aps(
    #         sound="default", # サウンド設定
    #         content_available=True, # onBackgroundMessage()を発火させるために必要
    #     )
    # )
    apns = messaging.APNSConfig(
    payload = messaging.APNSPayload(
    aps = messaging.Aps( content_available = True ) #　ここがバックグランド通知に必要な部分
    )
)
    # FCM通知メッセージの作成
    # message = messaging.Message(
    #     # notification=messaging.Notification(title=title, body=body),
    #     data={
    #         "content_available": "true",
    #         "title": title,
    #         "body": body
    #     },
    #     token=device_token,
    #     apns = apns
    # )
    # print(message)
    # 通知メッセージの作成
    notification = messaging.Notification(
        title=title,
        body=body
    )

    # データメッセージの作成
    data_message = messaging.Message(
        notification=notification,
        data={
            # "content_available": "true",
            "title": title,
            "body": body
        },
        token=device_token
    )
    response = messaging.send(data_message)
    # FCM通知の送信
    # response = messaging.send(message)
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

            print("afefe")
            # # ユーザーデータの遅延ロード
            # users = await load_users(db, content.group_id)
            # print(users)
            # print("users")
            # print(users[0].id)
            group_query = select(group_model.Group).filter(group_model.Group.id == content.group_id)
            result_group = await db.execute(group_query)
            group = result_group.scalars().first()
            print(group)
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
                if content.user_id == user.id:
                    # content.user_id == user.idのときスキップ　つまりチャットを送った人ならスキップ check1 未確認。
                    continue
                print(user.id)
                print(f"データー！{user.id}")
                # フォアグランド、個人チャンネルへプッシュ
                data = {
                    "id": user.id,
                    "name": "おためし",
                    "group_id": group_chat.group_id,
                    "user_id": group_chat.user_id,
                    # "user_id": group_chat.user_id,
                    "content": {
                        "group_chat_id": group_chat_content.group_chat_id,
                        "content_type": group_chat_content.content_type,
                        "text_content": group_chat_content.text_content,
                        "s3_object_key": group_chat_content.s3_object_key,
                        "id": group_chat_content.id
                    }
                }
                # userチャンネルにパブリッシュ
                room = f"user_chanel{user.id}"
                user_crud.publish_to_redis_for_user(room,data)

                # FCM 
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

        return group,group_chat
        # return "message 1"
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




# async def get_groups_with_latest_chat(db: AsyncSession, user_id: int):
#     # サブクエリを使って各グループごとの最新のチャットの日付を取得
#     latest_chats_subquery = (
#         select(
#             group_chat_model.GroupChat.group_id,
#             func.max(group_chat_model.GroupChat.created_at).label("latest_chat_date")
#         )
#         .group_by(group_chat_model.GroupChat.group_id)
#         .alias("latest_chats")
#     )

#     # グループと最新のチャットの日付を取得するクエリ
#     result = await db.execute(
#         select(group_model.Group, latest_chats_subquery.c.latest_chat_date)
#         .join(latest_chats_subquery, group_model.Group.id == latest_chats_subquery.c.group_id)
#         .options(joinedload(group_model.Group.group_chats).joinedload(group_chat_model.GroupChat.content))
#         .filter(group_model.Group.users.any(user_model.User.id == user_id))
#         .order_by(desc(latest_chats_subquery.c.latest_chat_date))
#     )

#     # 結果を取得
#     groups_with_latest_chat = result.all()
#     return groups_with_latest_chat


async def get_groups_with_latest_chat(db: AsyncSession,user_id):
    # async with db.begin():
    result_group = await db.execute(
        select(group_model.Group, func.max(group_chat_model.GroupChat.created_at).label("latest_chat_date"))
        .join(group_chat_model.GroupChat)
        .join(group_model.GroupUser)
        .filter(group_model.GroupUser.user_id == user_id)
        .group_by(group_model.Group.id)
        .order_by(desc("latest_chat_date"))
        .limit(10)
    )
    result_group_chat = await db.execute(
        select(group_chat_model.GroupChat)
        .join(group_model.Group)
        .order_by(desc(group_chat_model.GroupChat.created_at))
        .limit(20)
    )
    # groups_with_latest_chat = await result.scalars().all()
    groups_with_latest_chat = result_group.scalars().all()
    group_chats = result_group_chat.scalars().all()

    print(groups_with_latest_chat)
    print(group_chats)
    # groups_with_latest_chat.group_chats = group_chats
    # print(groups_with_latest_chat)
    # result = await db.execute(
    #     select(group_model.Group, func.max(group_chat_model.GroupChat.created_at).label("latest_chat_date"))
    #     .join(group_chat_model.GroupChat)
    #     .join(group_model.GroupUser)  # user_group_model.UserGroupによりユーザーとグループを結合
    #     .filter(group_model.GroupUser.user_id == user_id)  # 特定のユーザーに絞り込み
    #     .group_by(group_model.Group.id, group_chat_model.GroupChat.created_at)  # 追加: created_atをGROUP BYに含める
    #     .order_by(desc("latest_chat_date"))
    #     .options(
    #         joinedload(group_model.Group.group_chats)
    #         .joinedload(group_chat_model.GroupChat.content)
    #         .order_by(desc(group_chat_model.GroupChat.created_at))
    #         .limit(20)
    #         )  # Order group_chats within each group
    #     .limit(10)  #
    # )
    for group in groups_with_latest_chat:
        print(group)

    return groups_with_latest_chat,group_chats