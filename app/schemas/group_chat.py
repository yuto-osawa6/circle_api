from typing import Optional,List
from pydantic import BaseModel, Field
from .user import User

# class GroupChatBase(BaseModel):
#     message: str = Field(example="メッセージ")

# class GroupChatCreate(GroupChatBase):
#     # message: str = Field(example="メッセージ")
#     user_id: int
#     group_id: int
#     class Config:
#         orm_mode = True

class GroupChatContentCreate(BaseModel):
    group_id: int
    user_id: int
    content_type: str
    s3_object_key: str = None
    text_content: str = None
    class Config:
        orm_mode = True

class GroupChatContent(BaseModel):
    group_chat_id: int
    content_type: str
    s3_object_key: str = None
    text_content: str = None

class GroupChat(BaseModel):
    id:int
    group_id: int
    user_id: int
    content_type: str
    s3_object_key: str = None
    text_content: str = None

class GroupChatContent2(GroupChat):
    id:int
    group_chat_id: int
    content_type: str
    s3_object_key: str = None
    text_content: str = None


# class GroupWithLatestChat(BaseModel):
#     group_id: int
#     # 他に必要なフィールドがあれば追加

# class GroupChat(BaseModel):
#     id: int
#     group_id: int
#     user_id: int
#     created_at: datetime 

# class LatestChatListsResponse(BaseModel):
#     groups: List[GroupWithLatestChat]
#     group_chats: List[GroupChat]