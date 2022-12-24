from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(1024))
    title2 = Column(String(1024))

    done = relationship("Done", back_populates="task")


class Done(Base):
    __tablename__ = "dones"

    id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)

    task = relationship("Task", back_populates="done")