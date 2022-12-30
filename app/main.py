from typing import Optional
from fastapi import FastAPI, Depends
from app.routers import task
from app.cruds.user import get_user
from app.cruds.user import get_or_create_user

from sqlalchemy.ext.asyncio import AsyncSession

import app.cruds.task as task_crud
import app.cruds.user as user_crud
from app.db import get_db


app = FastAPI()
app.include_router(task.router)
# app.include_router(done.router)

@app.get("/")
def read_root():
    # return {"Hello": "World32"}
    return {"email": "World32","token2": "","afe":"afe"}

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

@app.get("/api/me")
async def list_tasks(db: AsyncSession = Depends(get_db),user = Depends(get_user)):
    print(user)
    return await user_crud.get_or_create_user(db,user)
    # get_or_create_user
    # return {"msg":"Hello, user","uid":user['uid']} 

