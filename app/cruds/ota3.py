
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


app = FastAPI()
def sample(**args):
    print(args)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print(websocket)