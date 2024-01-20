from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship

from app.models.group_chat import GroupChat
from app.models.tag import TagGroup 

from app.db import Base


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True, nullable=False)
    level = Column(Integer, nullable=False, default=0)
    description = Column(String(300))
    # 関連
    users = relationship('User', secondary="group_users", back_populates='groups', overlaps='group_users', lazy='selectin')
    # 
    group_users = relationship('GroupUser', back_populates='group', overlaps='groups,users')
    # 
    group_chats = relationship('GroupChat', back_populates='group')
    # 
    tag_groups = relationship('TagGroup', back_populates='group', overlaps='groups,tags')
    # group_users = relationship("GroupUser", back_populates="user", overlaps='groups,users')

    # tags = relationship('Tag', secondary="tag_groups", back_populates='groups', overlaps='tag_groups', lazy='selectin')
    tags = relationship('Tag', secondary="tag_groups", back_populates='groups', overlaps='tag_groups', lazy='selectin')
    # groups = relationship('Group', secondary="group_users", back_populates='users', overlaps='group_users', lazy='selectin')



class GroupUser(Base):
    __tablename__ = "group_users"
    # id = Column(Integer, primary_key=True, index=True)
    authority = Column(Integer, default=0, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    # 
    group = relationship("Group", back_populates="group_users", overlaps='groups,users')
    user = relationship("User", back_populates="group_users", overlaps='groups,users')

# class GroupDetails