from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship

from app.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String(768), unique=True, nullable=False)
    email = Column(String(768), unique=True, nullable=False)
    cid = Column(String(768), unique=True, nullable=False, index=True)
    first_time = Column(Boolean, nullable=False, default=False)
    # dfd = Column(String(768), unique=True, nullable=False, index=True)
    device_token = Column(String(768), unique=True, nullable=False)

    user_detail = relationship(
        "UserDetail", back_populates="user", uselist=False)
    # groups = relationship('Group', secondary="group_users", back_populates='users', overlaps='group_users')
    # groups = relationship('Group', secondary="group_users", back_populates='users', overlaps='group_users', lazy='selectin')
    groups = relationship('Group', secondary="group_users", back_populates='users', overlaps='group_users')


    # groups = relationship('Group', secondary="group_users")


    # 
    group_users = relationship("GroupUser", back_populates="user", overlaps='groups,users')
    # check1 overlap書いてない　(overlaps='users,groups') 入れといた　エラー確認してない。
    group_chats = relationship('GroupChat', back_populates='user',overlaps='users,groups')


class UserDetail(Base):
    __tablename__ = "user_details"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False,unique=True)
    name = Column(String(1024))

    user = relationship("User", back_populates="user_detail")
