from fastapi import FastAPI, WebSocket, APIRouter
import redis

app = FastAPI()
router = APIRouter()
redis_client = redis.Redis(host='redis', port=6379) #docker-container

# チャットルームに入ったらRedisのPubSubチャンネルにサブスクライブする
@app.websocket("/ws/{group_chat_id}/{user_id}")
# async def websocket_endpoint(websocket: WebSocket, group_chat_id: str, user_id: str):
async def websocket_endpoint(websocket: WebSocket, group_chat_id: str, user_id: str):
    await websocket.accept()

    # RedisのPubSubチャンネルにサブスクライブする
    channel = f"group_chat_room_{group_chat_id}"
    pubsub = redis_client.pubsub()
    pubsub.subscribe(channel)

    while True:
        # Redisからメッセージを受信する
        message = pubsub.get_message(ignore_subscribe_messages=True)

        # メッセージが存在する場合は、Websocketを介してクライアントに送信する
        if message:
            message_data = message["data"].decode()
            await websocket.send_text(message_data)


# メッセージを送信したらRedisのPubSubチャンネルにパブリッシュする
@router.post("/groups/{group_id}/group_chats")
async def send_message(group_id: str, message: str, user_id: str):
    # RedisのPubSubチャンネルにパブリッシュする
    channel = f"group_chat_channel_{group_id}"
    redis_client.publish(channel, f"{user_id}: {message}")

    return {"message": "OK"}
