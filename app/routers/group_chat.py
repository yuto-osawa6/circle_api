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
# security = HTTPBearer()
# logger = logging.getLogger(__name__)

async def on_connect(websocket: WebSocket):
    await websocket.accept()
# チャットルームに入ったらRedisのPubSubチャンネルにサブスクライブする
# @app.websocket("/ws/{group_chat_id}/{user_id}")
# # async def websocket_endpoint(websocket: WebSocket, group_chat_id: str, user_id: str):
# async def websocket_endpoint(websocket: WebSocket, group_chat_id: str, user_id: str):
#     print(999999999)
#     print(user_id)
#     await websocket.accept()
#     if not verify_user(user_id, group_chat_id):
#       logger = logging.getLogger(__name__)
#       logger.info(f"connection refused for user {user_id} and group chat {group_chat_id}")
#       await websocket.close(code=403)
#       return
#     # await on_connect(websocket)

#     # RedisのPubSubチャンネルにサブスクライブする
#     channel = f"group_chat_room_{group_chat_id}"
#     pubsub = redis_client.pubsub()
#     pubsub.subscribe(channel)

#     while True:
#         # Redisからメッセージを受信する
#         message = pubsub.get_message(ignore_subscribe_messages=True)

#         # メッセージが存在する場合は、Websocketを介してクライアントに送信する
#         if message:
#             message_data = message["data"].decode()
#             await websocket.send_text(message_data)

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     try:
#         await websocket.accept()
#     except Exception as e:
      
#         logger.error(f"An exception occurred while verifying user: {e}")
#         await websocket.close(code=500)
@router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket, extra_headers=[('Authorization', f'Bearer {jwt_token}')]):
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # print(websocket)
    # await websocket.send_text("Hello, server!")
    # data = await websocket.receive_text()
    data = await websocket.receive_text()
    await websocket.send_text(f"{data}")
    print(data)
    print("aaaaaaa")
    # await websocket.accept()
    # while True:
    #     data = await websocket.receive_text()
    #     await websocket.send_text(f"Message text was: {data}")

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket, token: HTTPAuthorizationCredentials = Depends(security)):
#     if not validate_token(token.credentials):
#         await websocket.close(code=HTTP_403_FORBIDDEN)
#         return
#     await websocket.accept()
#     while True:
#         try:
#             data = await websocket.receive_text()
#             await websocket.send_text(f"Message text was: {data}")
#         except WebSocketDisconnect:
#             break


# メッセージを送信したらRedisのPubSubチャンネルにパブリッシュする
@router.post("/groups/{group_id}/group_chats")
async def send_message(group_id: str, message: str, user_id: str):
    # RedisのPubSubチャンネルにパブリッシュする
    channel = f"group_chat_channel_{group_id}"
    redis_client.publish(channel, f"{user_id}: {message}")

    return {"message": "OK"}


# import redis

# redis_client = redis.Redis(host='redis', port=6379)

# # Pub/Subチャンネルにサブスクライブする
# channel = 'test_channel'
# pubsub = redis_client.pubsub()
# pubsub.subscribe(channel)

# # メッセージを送信する
# redis_client.publish(channel, 'Hello World!')

# # メッセージを受信する
# while True:
#     message = pubsub.get_message(ignore_subscribe_messages=True)
#     if message:
#         print(f"Received message: {message['data'].decode()}")
