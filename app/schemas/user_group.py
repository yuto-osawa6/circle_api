from pydantic import BaseModel
from typing import List, Type

class UserBase2(BaseModel):
    uid: str
    email: str
    cid: str
    device_token: str

class UserBase3(UserBase2):
    id: int
    first_time: bool

    class Config:
        orm_mode = True


class GroupUserBase(BaseModel):
    id: int
    name: str
    level: int
    # users: List[Type['User2']]  # 循環参照を回避するために Type['User2'] を使用
    users:  List[UserBase3]
    class Config:
        orm_mode = True

class User2(UserBase2):
    id: int
    first_time: bool
    groups: List[GroupUserBase]  # ユーザーが所属するグループのリスト

    class Config:
        orm_mode = True
