from typing import Optional,List
from pydantic import BaseModel, Field
from .user import User
# import app.schemas.user as user_scheme

# check-1 response model で返す場合もormmode true にしてる箇所があるので直す。

class GroupBase(BaseModel):
    name: str = Field(None, example="クリーニングを取りに行く")

class GroupCreate(GroupBase):
    level: int = Field(example=1)
    name:str

    # users: List[int] = Field(example=[1,2])

    class Config:
        orm_mode = True

class GroupCreateResponse(GroupCreate):
    id: int
    level: int = Field(example=1)
    name:str

    # class Config:
    #     orm_mode = True


class GroupUpdate(GroupBase):
    pass

class Group(GroupBase):
    id: int
    level: int
    # users: List[User]

    class Config:
        orm_mode = True

class ShowGroup(GroupBase):
    group: Group
    users: List[User]

# responce
class ReadUserGroup(BaseModel):
    groups: List[Group]

    class Config:
        orm_mode = True

class ReadUserGroupList(BaseModel):
    page: int

    class Config:
        orm_mode = True

# 追記
# class GroupUserBase(BaseModel):
#     id: int
#     name: str
#     level: int
#     users: List[user_scheme.User2]  # グループに所属するユーザーのリスト
    
