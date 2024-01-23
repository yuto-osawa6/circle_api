import pytest
from fastapi.testclient import TestClient
# from app.routers.group_chat import app
# from app.routers.group_chat import app
# from routers.group_chat import app
from app.main import app
# import asyncio
import websockets
import jwt


client = TestClient(app)

@pytest.mark.asyncio
async def test_websocket_endpoint():
    async with websockets.connect('ws://localhost:8080/ws') as websocket:
        
        print("Connected to websocket")
        await websocket.send("Hello, client!")
        data = await websocket.recv()
        print("データーよ。")
        print(data)
        print("データーよ。")
        assert data == "Hello, client!"

        # await asyncio.sleep(0.1)
    # assert websocket.closed

# import os
# import pytest
# import websockets

# @pytest.mark.asyncio
# async def test_websocket_endpoint():
#     # JWTトークンを取得
#     jwt_token = "your_jwt_token_here"
    
#     # WebSocket接続時にAuthorizationヘッダーにトークンを設定
#     async with websockets.connect('ws://localhost:8080/ws', extra_headers=[('Authorization', f'Bearer {jwt_token}')]) as websocket:
#         print("Connected to websocket")
#         await websocket.send("Hello, server!")
#         data = await websocket.recv()
#         assert data == "Hello, client!"


def test_addition():
    print("データーよ2。")
    assert 2 + 2 == 4

def test_subtraction():
    assert 5 - 3 == 2

def test_multiplication():
    assert 5 * 5 == 25

def test_division():
    assert 10 / 2 == 5