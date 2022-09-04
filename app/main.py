from typing import Optional
from fastapi import FastAPI, Depends
from app.routers import task
from app.cruds.user import get_user

app = FastAPI()
app.include_router(task.router)
# app.include_router(done.router)

@app.get("/")
def read_root():
    return {"Hello": "World32"}

@app.get("/product")
def read_root():
  return {"aee":"aee"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/api/me")
async def hello_user(user = Depends(get_user)):
    # print(user)
    return {"msg":"Hello, user","uid":user['uid']} 