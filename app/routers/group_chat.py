from fastapi import FastAPI, WebSocket
import redis

app = FastAPI()
redis_client = redis.Redis(host='redis', port=6379) #docker-container

@app.websocket("/ws/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, user_id: str):
    await websocket.accept()

    channel = f"room:{room_id}"
    redis_client.publish(channel, f"{user_id} has joined the room")

    while True:
        message = await websocket.receive_text()
        redis_client.publish(channel, f"{user_id}: {message}")

@app.on_event("startup")
async def startup_event():
    redis_client.flushdb()