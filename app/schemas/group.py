from typing import Optional,List
from pydantic import BaseModel, Field
# from .user import User

class GroupBase(BaseModel):
    name: str = Field(None, example="クリーニングを取りに行く")

class GroupCreate(GroupBase):
    level: int = Field(example=1)
    name:str

    # users: List[int] = Field(example=[1,2])

    class Config:
        orm_mode = True

# class GroupCreateResponse(GroupCreate):
#     id: int
#     level: int = Field(example=1)
#     name:str

#     class Config:
#         orm_mode = True


class GroupUpdate(GroupBase):
    pass

class Group(GroupBase):
    id: int
    level: int
    users: List["User"] = []

    class Config:
        orm_mode = True