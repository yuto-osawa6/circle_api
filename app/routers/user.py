from typing import List
# from fastapi import APIRouter
import app.schemas.task as task_schema
import logging
from fastapi import APIRouter,FastAPI, Depends, Header, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

# import app.cruds.task as task_crud
import app.cruds.user as user_crud
from app.db import get_db
import redis
import asyncio


router = APIRouter()
redis_client = redis.Redis(host='redis', port=6379) #docker-container

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

connected_users = set()

# user チャンネル用
@router.websocket("/ws/users/{user_id}")
async def websocket_endpoint(websocket: WebSocket,user_id: int, db: AsyncSession = Depends(get_db)):
# async def websocket_endpoint(websocket: WebSocket,group_id: int,user_id: int, db: AsyncSession = Depends(get_db)):
    await websocket.accept()
    pubsub = redis_client.pubsub()
    pubsub.subscribe(f"user_chanel{user_id}")

    # WebSocket接続が確立されたときにユーザーをセットに追加
    connected_users.add(user_id)
    # print("connected_users({connected_users})")
    # data = await websocket.receive_text()
    # await websocket.send_text(f"{data}")
    # print(data)
    # print("user_chanel{user_id}")
    # logger.info('WebSocket connection establishedおおお')
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
        # logger.info('WebSocket connection establishedおおお22')
    finally:
        # WebSocket接続が閉じられたときにセットからユーザーを削除
        connected_users.remove(user_id)

        # WebSocket接続を閉じる前にRedisのサブスクリプションを解除する
        pubsub.unsubscribe(f"user_chanel{user_id}")

@router.put("/users/{user_id}/device_token")
async def update_device_token(user_id: int,db: AsyncSession = Depends(get_db),device_token: str = Header(...)):
    return await user_crud.update_fcm_token_crud(db,user_id,device_token)