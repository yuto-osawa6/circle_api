from typing import Optional
from pydantic import BaseModel, Field
from typing import List
# import app.models.group as Group
# from app.schemas.group import GroupUserBase
# import app.schemas.group as group_scheme


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

# 追記2

# class UserBase2(BaseModel):
#     uid: str
#     email: str
#     cid: str
#     device_token: str

# class User2(UserBase2):
#     id: int
#     first_time: bool
#     groups: List[group_scheme.GroupUserBase]  # ユーザーが所属するグループのリスト

#     class Config:
#         orm_mode = True