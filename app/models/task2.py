from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


class Task(Base):
    __tablename__ = "atasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    title2 = Column(String(1024))
    title3 = Column(String(1024))
    title4 = Column(String(1024))
    title5 = Column(String(1024))
    # title6 = Column(String(1024))


    done = relationship("Adone", back_populates="atask")


class Done(Base):
    __tablename__ = "adones"

    id = Column(Integer, ForeignKey("atasks.id"), primary_key=True)

    task = relationship("Atask", back_populates="adone")


# 1対１

# class Group(Base):
#     __tablename__ = "groups"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True, index=True)
#     is_active = Column(Boolean, default=True)
#     detail = relationship('GroupDetail', back_populates='group', uselist=False)

# class GroupDetail(Base):
#     __tablename__ = "group_details"

#     id = Column(Integer, primary_key=True, index=True)
#     description = Column(String)
#     group_id = Column(Integer, ForeignKey('groups.id'), unique=True)
#     group = relationship('Group', back_populates='detail')

# 1対多
# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)
#     is_active = Column(Boolean, default=True)
#     tasks = relationship('Task', back_populates='user')

# class Task(Base):
#     __tablename__ = "tasks"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     is_done = Column(Boolean, default=False)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     user = relationship('User', back_populates='tasks')

# 多対多

# class Book(Base):
#     __tablename__ = "books"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     is_available = Column(Boolean, default=True)
#     authors = relationship("BookAuthor", back_populates="book")

# class Author(Base):
#     __tablename__ = "authors"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True, index=True)
#     biography = Column(String)
#     books = relationship("BookAuthor", back_populates="author")

# class BookAuthor(Base):
#     __tablename__ = "book_authors"

#     id = Column(Integer, primary_key=True, index=True)
#     book_id = Column(Integer, ForeignKey("books.id"))
#     author_id = Column(Integer, ForeignKey("authors.id"))

#     book = relationship("Book", back_populates="authors")
#     author = relationship("Author", back_populates="books")

# create

# @app.post("/users/")
# async def create_user(user: UserCreate):
#     async with async_session() as session:
#         db_user = User(**user.dict())
#         session.add(db_user)
#         await session.commit()
#         await session.refresh(db_user)
#         return db_user

# delete
# @app.delete("/users/{user_id}")
# async def delete_user(user_id: int):
#     async with async_session() as session:
#         user = await session.get(User, user_id)
#         if user is None:
#             return {"error": "User not found"}
#         session.delete(user)
#         await session.commit()
#         return {"message": "User deleted successfully"}

# get
# @app.get("/users/{user_id}", response_model=UserOut)
# async def read_user(user_id: int):
#     async with async_session() as session:
#         user = await session.get(User, user_id)
#         if user is None:
#             return {"error": "User not found"}
#         return user]


# from typing import List, Optional
# from pydantic import BaseModel

# class ItemBase(BaseModel):
#     name: str
#     price: float
#     description: Optional[str] = None

# class ItemCreate(ItemBase):
#     pass

# class ItemUpdate(ItemBase):
#     pass

# class Item(ItemBase):
#     id: int

#     class Config:
#         orm_mode = True




