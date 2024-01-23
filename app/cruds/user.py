from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Response
from firebase_admin import auth, credentials
import firebase_admin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,desc,func
from sqlalchemy.orm import selectinload,subqueryload,joinedload
from sqlalchemy.sql import text
from fastapi.encoders import jsonable_encoder

# import app.models.task as task_model
# import app.schemas.task as task_schema
import app.models.user as user_model
import app.models.group as group_model
import app.models.group_chat as group_chat_model
import app.schemas.user as user_schema
from sqlalchemy.engine import Result
from typing import List, Tuple, Optional
import uuid
import requests

import json
import redis

# cred = credentials.Certificate('./account_key.json')
# app/account_key.json
cred = credentials.Certificate('./app/account_key.json')
firebase_admin.initialize_app(cred)

redis_client = redis.Redis(host='redis', port=6379)


def get_user(res: Response, cred: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))):
    print("cred")
    print(cred is None)
    print("cred")
    if cred is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication required",
            headers={'WWW-Authenticate': 'Bearer realm="auth_required"'},
        )
    try:
        print("cred2")
        print(cred)
        decoded_token = auth.verify_id_token(cred.credentials)
        print(decoded_token)
        # print(decoded_token) 
        print("aefijaeiofjaoifje")
        print(decoded_token['uid'])
        print(decoded_token['email'])
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials. {err}",
            headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
        )
    res.headers['WWW-Authenticate'] = 'Bearer realm="auth_required"'
    return decoded_token

# async def get_or_create_user(db: AsyncSession,res: Response, cred: HTTPAuthorizationCredentials=Depends(HTTPBearer(auto_error=False))):
#     if cred is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Bearer authentication required",
#             headers={'WWW-Authenticate': 'Bearer realm="auth_required"'},
#         )
#     try:
#         print(cred)
#         decoded_token = auth.verify_id_token(cred.credentials)

#         result: Result = await db.execute(
#         select(user_model.User).filter(
#             user_model.User.uid == decoded_token['uid'],
#             user_model.User.email == decoded_token['email']
#             )
#         )
#         user: Optional[Tuple[user_model.User]] = result.first()


#         # print(user)
#         # print(user[0] if user is not None else None)
#         if user == None:
#             print("No")
#             # create
#             user = user_model.User(
#                 uid = decoded_token['uid'],
#                 email = decoded_token['email']
#             )
#             db.add(user)
#             await db.commit()
#             await db.refresh(user)
#             return user
#         pass

#         print(user)
#         print(user[0] if user is not None else None)

#         print(decoded_token['uid'])
#         print(decoded_token['email'])

#         print("aefijaeiofjaoifje")
#     except Exception as err:
#         # 通信エラーの場合
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=f"Invalid authentication credentials. {err}",
#             headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
#         )
#     res.headers['WWW-Authenticate'] = 'Bearer realm="auth_required"'
#     return user


async def get_or_create_user(db: AsyncSession, decoded_token, device_token: str):
    print(decoded_token)
    try:
        result = await db.execute(
            select(user_model.User).filter(
                user_model.User.uid == decoded_token['uid'],
                user_model.User.email == decoded_token['email']
            )
        )
        user: Optional[user_model.User] = result.scalar_one_or_none()

        if user == None:
            print("No")
            # create
            user = user_model.User(
                uid=decoded_token['uid'],
                email=decoded_token['email'],
                cid=str(uuid.uuid4()),
                device_token=device_token  # デバイストークンを設定
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user
        else:
            # groupsの数の制限取得
            # groups_query2 = select(group_model.Group).limit(20)
            # groups_query = await db.execute(groups_query2)
            # user.groups = groups.scalars().all()
            # グループの取得、最新のチャットがある順に。
            # groups_query = (
            #     select(group_model.Group, func.max(group_chat_model.GroupChat.created_at).label("latest_chat_date"))
            #     # .join(user_model.User)
            #     .join(group_chat_model.GroupChat, group_model.Group.id == group_chat_model.GroupChat.group_id)
            #     .join(group_model.GroupUser)
            #     .filter(group_model.GroupUser.user_id == user.id)
            #     .group_by(group_model.Group.id)
            #     .order_by(desc("latest_chat_date"))
            #     .limit(10)
            # )
            groups_query = (
                select(group_model.Group, func.max(group_chat_model.GroupChat.created_at).label("latest_chat_date"))
                .join(group_chat_model.GroupChat, group_model.Group.id == group_chat_model.GroupChat.group_id)
                .join(group_model.GroupUser)
                .filter(group_model.GroupUser.user_id == user.id)
                .group_by(group_model.Group.id)
                .order_by(desc("latest_chat_date"))
                .limit(10)
            )
            result_groups = await db.execute(groups_query)
            print("Before assigning user.groups:", user.groups)
            # user.groups = groups_result.scalars().all()
            # print("After assigning user.groups:", user.groups)
            # user.groups = result_groups.scalars().all()
            # print(f"user.groups:{user.groups}")
            # print(groups)
            latest_group_ids2 = [group.id for group in result_groups]
            print(f"latest_group_ids2:{latest_group_ids2}")
            subquery = (
                select(
                    group_chat_model.GroupChat,
                    func.row_number().over(
                        partition_by=group_chat_model.GroupChat.group_id,
                        order_by=text("created_at DESC")
                    ).label("row_num")
                )
                .filter(group_chat_model.GroupChat.group_id.in_(latest_group_ids2))
                .alias("subquery")
            )
            # メインクエリでサブクエリを使用して最新の10件を取得
            # checkt 10指定
            chats_query = (
                select(group_chat_model.GroupChat)
                .join(subquery, group_chat_model.GroupChat.id == subquery.c.id)
                # .options(selectinload(group_chat_model.GroupChat.content))
                .where(subquery.c.row_num <= 10)
                .order_by(
                    subquery.c.group_id,
                    subquery.c.created_at.desc()
                )
            )
            result_chats = await db.execute(chats_query)
            chats = result_chats.scalars().all()
            # 新規メッセージの取得
            
            # ユーザーが既に存在する場合はデバイストークンを更新
            if user.device_token != device_token:
                user.device_token = device_token
                await db.commit()
                await db.refresh(user)

        print("user:")
        print("aefijaeiofjaoifje")
    except Exception as err:
        # 通信エラーの場合
        print("エラーが起きました。milk")
        print(err)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials. {err}",
            headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
        )
    return user,result_groups,chats


async def get_user2(db: AsyncSession, decoded_token):
    print(decoded_token)
    print("print(decoded_token)")
    try:
        result: Result = await db.execute(
            select(user_model.User).filter(
                user_model.User.uid == decoded_token['uid'],
                user_model.User.email == decoded_token['email']
            )
        )
        # print(f"user1:{result.all()}")
        # print(f"user2:{result.first()}")
        user: Optional[Tuple[user_model.User]] = result.first()
        print(user)
        print(user[0] if user is not None else None)
        if user is None:
            raise HTTPException(status_code=404, detail='User not found')
        # # pass
        print(f"user:{user}")
        print(f"user:{user[0]}")

        return user[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail='Server Error')
    
# async def get_user_by_token(db: AsyncSession,res: Response, cred: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))):
#     if cred is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Bearer authentication required",
#             headers={'WWW-Authenticate': 'Bearer realm="auth_required"'},
#         )
#     try:
#         print(cred)
#         decoded_token = auth.verify_id_token(cred.credentials)
#         # print(decoded_token)
#         print("aefijaeiofjaoifje")
#         print(decoded_token['uid'])
#         print(decoded_token['email'])
#     except Exception as err:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=f"Invalid authentication credentials. {err}",
#             headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
#         )
#     res.headers['WWW-Authenticate'] = 'Bearer realm="auth_required"'
#     try:
#         result: Result = await db.execute(
#             select(user_model.User).filter(
#                 user_model.User.uid == decoded_token['uid'],
#                 user_model.User.email == decoded_token['email']
#             )
#         )
#         user: Optional[Tuple[user_model.User]] = result.first()
#         if user == None:
#             raise HTTPException(status_code=404, detail='User not found')
#         # # pass
#         # return user[0]
#         return user_schema.User(uid=decoded_token['uid'], email=decoded_token['email'])
#     except Exception as e:
#         raise HTTPException(status_code=500, detail='Server Error')



async def update_fcm_token_crud(db:AsyncSession,user_id:int,device_token: str):
    try:
        # # ユーザーを探す
        user = await db.execute(select(user_model.User).filter(user_model.User.id == user_id))
        user = user.scalar()
        print(user.device_token)

        # ユーザーが存在する場合にデバイストークンを更新
        if user:
            user.device_token = device_token
            await db.commit()
            await db.refresh(user)
            return {"status": "Device token updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail='Server Error')
    
    # ユーザーが存在しない場合や処理が実行されなかった場合はエラーを返す
    raise HTTPException(status_code=404, detail='User not found')


# user チャンネルにパブリッシュする関数
def publish_to_redis_for_user(channel, data):
    redis_client.publish(channel, json.dumps(data))