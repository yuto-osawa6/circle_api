from typing import Optional
from fastapi import FastAPI, Depends, Header
from app.routers import task,group,group_chat,user
from app.cruds.user import get_user
from app.cruds.user import get_or_create_user

from sqlalchemy.ext.asyncio import AsyncSession

import app.cruds.task as task_crud
import app.cruds.user as user_crud
# scheme
import app.schemas.user_group  as user_group_scheme
from app.db import get_db
import redis
# from fastapi.logger import logger as fastapi_logger
# from fastapi.logger import logger as fastapi_logger
# from uvicorn import logger as uvicorn_logger
import logging


app = FastAPI()
app.include_router(task.router)
app.include_router(group.router)
app.include_router(group_chat.router)
app.include_router(user.router)

# app.inclute

redis_client = redis.Redis(host='redis', port=6379) #docker-container

fastapi_logger = logging.getLogger("fastapi")
fastapi_logger.setLevel(logging.DEBUG)
# print(redis_client.ping())
# print("aaaaa")

# app.include_router(done.router)

@app.get("/")
def read_root():
    # return {"Hello": "World32"}
    print(redis_client.ping())
    print("aaaaa")
    return {"email": "World32","token2": "","afe":"afe"}

# @app.get("/hello")
# def hello():
#     return{"a":"hello"}


# @app.get("/ota")
# def read_root():
#     # return {"Hello": "World32"}
#     return {"email": "World32","token2": "","afe":"afe"}

# @app.get("/ota")
# async def list_tasks(db: AsyncSession = Depends(get_ota)):
#     return await task_crud.get_tasks_with_done(db)


@app.get("/product")
def read_root():
  return {"aee":"aee"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

# @app.get("/api/me")
# async def hello_user(user = Depends(get_user)):
#     print(user)
#     return {"msg":"Hello, user","uid":user['uid']} 

# @app.get("/api/me")
# async def list_tasks(db: AsyncSession = Depends(get_db)):
#     return await user_crud.get_or_create_user(db)

# @app.get("/api/me",response_model = user_group_scheme.User2)
@app.get("/api/me")
async def list_tasks(db: AsyncSession = Depends(get_db),user = Depends(get_user),device_token: str = Header(...)):
    # print(user)
    print(f"device:{device_token}")
    print(f"aaaaafefefae")
    # a,b=  await user_crud.get_or_create_user(db,user,device_token)
    # # user_dict = 
    # # return await user_crud.get_or_create_user(db,user,device_token)
    # print(f"user.groups2:{a.groups}")
    # # print(f"user.groups3:{a.dict()}")


    # return {"user":a,"group_chats":b}
    # return b
    # return {"user": a, "group_chats": b}
    try:
        a, b,c = await user_crud.get_or_create_user(db, user, device_token)
        # a = await user_crud.get_or_create_user(db, user, device_token)

        # print(f"user.groups2:{a.groups}")
        print("User object:")
        # for user_obj in a:
        # print(a.dict())
        return {"user": a , "groups": b,"group_chats": c}
    except Exception as e:
        print(f"get_or_create_user でエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()


