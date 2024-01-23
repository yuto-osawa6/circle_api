



from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship

from app.models.group_chat import GroupChat

from app.db import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    # tag_name 制約注意 
    tag_name = Column(String(30), index=True, nullable=False)
    groups = relationship('Group', secondary="tag_groups", back_populates='tags', overlaps='tag_groups', lazy='selectin')
    # 
    tag_groups = relationship('TagGroup', back_populates='tag', overlaps='groups,tags')
    # 
    # group_chats = relationship('GroupChat', back_populates='group')

# 中間テーブル
class TagGroup(Base):
    __tablename__ = "tag_groups"
    # id = Column(Integer, primary_key=True, index=True)
    # authority = Column(Integer, default=0, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)

    # 
    group = relationship("Group", back_populates="tag_groups", overlaps='groups,tags')
    tag = relationship("Tag", back_populates="tag_groups", overlaps='groups,tags')