# from fastapi import FastAPI, WebSocket, APIRouter
import redis
import logging
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, APIRouter,Query, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.status import HTTP_403_FORBIDDEN
# logger = logging.getLogger(__name__)
import secrets
import jwt
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db

import app.cruds.group_chat as group_chat_crud
import app.schemas.group_chat as group_chat_scheme
import asyncio

# import app.cruds.user as user_crud

# from app.main import app



# SECRET_KEY = secrets.token_hex(32)

# # JWTのペイロードを定義する
# payload = {"sub": "1234567890", "name": "John Doe", "iat": 1516239022}

# # JWTを署名する
# jwt_token = jwt.encode(payload, "secret_key", algorithm="HS256")

# app = FastAPI()

# origins = [
#     "*"
#     # "http://localhost",
#     # "http://localhost:8080",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

router = APIRouter()
redis_client = redis.Redis(host='redis', port=6379) #docker-container
print(redis_client.ping())
print("aaaaa")


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

async def on_connect(websocket: WebSocket):
    await websocket.accept()



@router.websocket("/ws/groups/{group_id}/{user_id}")
# async def websocket_endpoint(websocket: WebSocket, extra_headers=[('Authorization', f'Bearer {jwt_token}')]):
async def websocket_endpoint(websocket: WebSocket,group_id: int,user_id: int, db: AsyncSession = Depends(get_db)):
    await websocket.accept()
    pubsub = redis_client.pubsub()
    pubsub.subscribe(f"group_chanel{group_id}")
    # data = await websocket.receive_text()
    # await websocket.send_text(f"{data}")
    # print(data)
    print("aaaaaaa２8")
    logger.info('WebSocket connection establishedおおお')
    try:
        while True:
            # logger.info("kokojoioijoiっっっっっっっkじょおいじおじょいじおじょいじょ")
            message = pubsub.get_message()
            # logger.info(message)
            # logger.info(message['data'].decode('utf-8'))
            if message and message['type'] == 'message':
                await websocket.send_text(message['data'].decode('utf-8'))

            await asyncio.sleep(0.1)  # 0.1秒待つ
    except AttributeError:
        print("Error: message data is not a byte string")
        logger.info('WebSocket connection establishedおおお22')
    finally:
        # WebSocket接続を閉じる前にRedisのサブスクリプションを解除する
        pubsub.unsubscribe(f"group_chanel{group_id}")



# @router.post("/groups/{group_id}/group_chats")
# async def create_message(body: group_chat_scheme.GroupChatContentCreate, db: AsyncSession = Depends(get_db)):
#     print(body)
#     room = f"group_chanel{body.group_id}"
#     db_message = await group_chat_crud.create_group_chat_content(db, body)
#     print(db_message)
#     print("aaaaa")
#     # redis_client.publish(room, f"{db_message.id}:{db_message.message}")
#     return "db_message"

@router.post("/groups/{group_id}/group_chats")
async def create_message(body: group_chat_scheme.GroupChatContentCreate, db: AsyncSession = Depends(get_db)):
    print("afefae22")
    # return await group_chat_crud.create_group_chat_content(db, body)
    try:
    # create_group_chat_contentの呼び出しを行う部分
        groups,group_chat = await group_chat_crud.create_group_chat_content(db, body)
        return {"groups":groups,"group_chats":group_chat}
    except Exception as e:
        print(f"Error in create_message: {e}")
        raise
# @router.post("/groups/{group_id}/group_chats")
# async def create_message(group_id: int, user_id: int, request: Request):
#     body = await request.json()
#     print("Request Body:", body)
#     # ここでcreate_group_chat_contentの呼び出しを行うなどの処理を行う
#     return {"status": "success"}

@router.get("/groups/{group_id}/group_chats")
async def read_group_chats(
    group_id: int, page:int = 1, db:  AsyncSession = Depends(get_db)
):
    # query = (
    #     db.query(GroupChat)
    #     .join(GroupChatContent)
    #     .filter(GroupChat.group_id == group_id)
    #     .offset(skip)
    #     .limit(limit)
    #     .all()
    # )
    return  await group_chat_crud.get_group_chats(db,group_id,page)



# check 1 ユーザーとのダイレクトメッセージもここに追加したいので、groupだけでなくuserとのチャットも加える。
# response_modelはあとで
@router.get("/latest_chat_lists",)
async def get_groups_with_latest_chat_route(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    # current_user = response_model.
):
    groups,group_chat= await group_chat_crud.get_groups_with_latest_chat(db,  user_id)
    print("groups_with_latest_chat")
    # print(groups_with_latest_chat)
    # groups_list = list(groups_with_latest_chat)

    # # リストの長さを表示
    # print(groups_list)
    # print(len(groups_list))
    # print(len(groups_with_latest_chat))
    return {"groups":groups,"group_chats":group_chat}