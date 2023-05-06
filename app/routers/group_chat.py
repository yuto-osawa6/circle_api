# from fastapi import FastAPI, WebSocket, APIRouter
import redis
import logging
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, APIRouter,Query
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

# @router.websocket("/ws")
# # async def websocket_endpoint(websocket: WebSocket, extra_headers=[('Authorization', f'Bearer {jwt_token}')]):
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     # print(websocket)
#     # await websocket.send_text("Hello, server!")
#     # data = await websocket.receive_text()
#     data = await websocket.receive_text()
#     await websocket.send_text(f"{data}")
#     print(data)
#     print("aaaaaaa")

@router.websocket("/ws/{group_id}/{user_id}")
# async def websocket_endpoint(websocket: WebSocket, extra_headers=[('Authorization', f'Bearer {jwt_token}')]):
async def websocket_endpoint(websocket: WebSocket,group_id: int,user_id: int, db: AsyncSession = Depends(get_db)):
    await websocket.accept()
    pubsub = redis_client.pubsub()
    pubsub.subscribe(f"group_chanel{group_id}")
    data = await websocket.receive_text()
    await websocket.send_text(f"{data}")
    print(data)
    print("aaaaaaa２8")
    logger.info('WebSocket connection establishedおおお')
    # try:
    while True:
        message = pubsub.get_message()
        print(message)
        print("aaa234")
        if message and message['type'] == 'message':
            await websocket.send_text(message['data'].decode('utf-8'))

        data = await websocket.receive_text()
        print(data)

    # except WebSocketDisconnect:
    #     pass

    # finally:
    #     # if pubsub is not None:
    #     #   await pubsub.unsubscribe()
    #     #   await pubsub.close()
    #       print("finallyブロック内の処理完了")

# # メッセージを送信したらRedisのPubSubチャンネルにパブリッシュする
# @router.post("/groups/{group_id}/group_chats")
# async def send_message(group_id: str, message: str, user_id: str):
#     # RedisのPubSubチャンネルにパブリッシュする
#     channel = f"group_chat_channel_{group_id}"
#     redis_client.publish(channel, f"{user_id}: {message}")

#     return {"message": "OK"}


@router.post("/groups/{group_id}/group_chats")
async def create_message(body: group_chat_scheme.GroupChatContentCreate, db: AsyncSession = Depends(get_db)):
    room = f"group_chanel{body.group_id}"
    db_message = await group_chat_crud.create_group_chat_content(db, body)
    redis_client.publish(room, f"{db_message.id}:{db_message.message}")
    return db_message