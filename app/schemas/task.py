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



class TaskBase(BaseModel):
    title: Optional[str] = Field(None, example="クリーニングを取りに行く")


class TaskCreate(TaskBase):
    pass


class TaskCreateResponse(TaskCreate):
    id: int

    # class Config:
    #     orm_mode = True


class Task(TaskBase):
    id: int
    # title2: str
    done: int = Field(1, description="完了フラグ")

    # class Config:
        # orm_mode = True

class Task():
    id: int
        # title2: str
    done: int = Field(1, description="完了フラグ")