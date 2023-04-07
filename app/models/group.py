from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship

from app.db import Base


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True, nullable=False)
    level = Column(Integer, nullable=False, default=0)

    # users = relationship('User', back_populates='group')
    users = relationship('User', secondary="group_users", back_populates='groups')

    # group = relationship("User", secondary="group_user", back_populates="user")
    # detail = relationship('GroupDetail', back_populates='group', uselist=False)

    # 
    group_users = relationship('GroupUser', back_populates='group')


class GroupUser(Base):
    __tablename__ = "group_users"
    # id = Column(Integer, primary_key=True, index=True)
    authority = Column(Integer, default=0, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    # 
    group = relationship("Group", back_populates="group_users")
    user = relationship("User", back_populates="group_users")

# class GroupDetails