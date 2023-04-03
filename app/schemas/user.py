from typing import Optional
from pydantic import BaseModel, Field


# class Task(BaseModel):
#     id: int
#     title: Optional[str] = Field(None, example="クリーニングを取りに行く2")
#     done: bool = Field(False, description="完了フラグ")

# class TaskCreate(Task):
#     pass

# class TaskCreateResponse(TaskCreate):
#     id: int

#     class Config:
#         orm_mode = True



class UserBase(BaseModel):
    # title: Optional[str] = Field(None, example="クリーニングを取りに行く")
    id:int

class UserCreate(UserBase):
    pass


class UserCreateResponse(UserCreate):
    id: int

    # class Config:
    #     orm_mode = True


class User(UserBase):
    id: int
    # title2: str
    # done: int = Field(1, description="完了フラグ")

    # class Config:
        # orm_mode = True

class User():
    id: int
        # title2: str
    # done: int = Field(1, description="完了フラグ")