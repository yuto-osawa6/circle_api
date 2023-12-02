from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Response
from firebase_admin import auth, credentials
import firebase_admin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload,subqueryload,joinedload
from fastapi.encoders import jsonable_encoder
# import app.models.task as task_model
# import app.schemas.task as task_schema
import app.models.user as user_model
import app.models.group as group_model
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
    print(cred is None)
    print("cred")
    if cred is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication required",
            headers={'WWW-Authenticate': 'Bearer realm="auth_required"'},
        )
    try:
        print(cred)
        decoded_token = auth.verify_id_token(cred.credentials)
        # print(decoded_token)
        print("aefijaeiofjaoifje")
        print(decoded_token['uid'])
        print(decoded_token['email'])
    except Exception as err:
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
        # result: Result = await db.execute(
        #     select(user_model.User).filter(
        #         user_model.User.uid == decoded_token['uid'],
        #         user_model.User.email == decoded_token['email']
        #     )
        #     # .options(selectinload(user_model.User.groups))
        #     # .options(subqueryload(user_model.User.groups).subqueryload(group_model.Group.users))  # ユーザーが所属するグループとグループに所属するユーザーの情報を一度に取得)
        #     # .options(selectinload(user_model.User.groups).selectinload(group_model.Group.users))
        #     .options(
        #         # selectinload(user_model.User.groups)
        #         # .limit(20)
        #         # .selectinload(group_model.Group.group_chats)
        #         # .selectinload(group_model.GroupChat.content),
        #         # selectinload(user_model.User.groups)
        #         # .limit(20)
        #         # .selectinload(group_model.Group.users)
        #         # joinedload(user_model.User.groups)
        #         # .joinedload(group_model.Group.group_chats)
        #         # .joinedload(group_model.GroupChat.content)
        #         # .subqueryload(group_model.GroupChatContent.group_chat),
        #         # joinedload(user_model.User.groups).limit(10)
        #         joinedload(user_model.User.groups).limit(10)
        #         # .joinedload(group_model.Group.users)
        #     )
        # )

        # user: Optional[Tuple[user_model.User]] = result.first()
        result = await db.execute(
            select(user_model.User).filter(
                user_model.User.uid == decoded_token['uid'],
                user_model.User.email == decoded_token['email']
            )
            # .options(
            #     joinedload(user_model.User.groups).limit(10)
            # )
        )
        user: Optional[user_model.User] = result.scalar_one_or_none()

        # print(user)
        # print(f"user0:{vars(user.groups[0])}")
        # print(f"user0:{vars(user.groups[0].users[0])}")
        # print(f"user1:{user}")
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
            # groupsの数の制限
            groups_query = select(group_model.Group).join(user_model.User.groups).where(user_model.User.id == user.id).limit(20)
            groups = await db.execute(groups_query)
            user.groups = groups.scalars().all()
            # ユーザーが既に存在する場合はデバイストークンを更新
            if user.device_token != device_token:
                user.device_token = device_token
                await db.commit()
                await db.refresh(user)

        print("user:")
        # print(vars(user[0]))
        # print()
        # print(f"user:{user}")
        # print(user[0])
        # print(vars(user[0]))
        # print("aa")

        # print(user[0] if user is not None else None)

        # print(decoded_token['uid'])
        # print(decoded_token['email'])

        print("aefijaeiofjaoifje")
        # return user[0]
    except Exception as err:
        # 通信エラーの場合
        print("エラーが起きました。milk")
        print(err)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials. {err}",
            headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
        )
    # res.headers['WWW-Authenticate'] = 'Bearer realm="auth_required"'
    # user_json = json.dumps(user, default=lambda o: o.__dict__)
    # return user_json
    return user


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