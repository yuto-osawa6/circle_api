from typing import Optional
from fastapi import FastAPI
# from routers import task

app = FastAPI()
# app.include_router(task.router)
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