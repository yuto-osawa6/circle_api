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


    done = relationship("Adone", back_populates="atask")


class Done(Base):
    __tablename__ = "adones"

    id = Column(Integer, ForeignKey("atasks.id"), primary_key=True)

    task = relationship("Atask", back_populates="adone")