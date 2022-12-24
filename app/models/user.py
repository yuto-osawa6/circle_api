from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, index=True)
    uid = Column(Integer)
    email = Column(String)
    # title2 = Column(String(1024))

#     done = relationship("Done", back_populates="task")


class UserDetail(Base):
    __tablename__ = "user_details"

    id = Column(Integer, primary_key = True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    name = Column(String(100))

    # task = relationship("Task", back_populates="done")