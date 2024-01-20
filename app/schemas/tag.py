from pydantic import BaseModel
from typing import List

class TagBase(BaseModel):
    id: int
    tag_name: str

class TagCreateBase(BaseModel):
    tag_name: str

# class TagCreate(TagBase):
#     pass