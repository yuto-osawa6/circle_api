from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db import Base


class GroupChat(Base):
    __tablename__ = "group_chats"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)  # 作成時の日付を保存するカラム
    # その他のカラム

    group = relationship("Group", back_populates="group_chats")
    user = relationship("User", back_populates="group_chats")

    content = relationship(
        "GroupChatContent", back_populates="group_chat", uselist=False)


class GroupChatContent(Base):
    __tablename__ = "group_chat_contents"

    id = Column(Integer, primary_key=True, index=True)
    group_chat_id = Column(Integer, ForeignKey(
        "group_chats.id"), nullable=False, unique=True)
    content_type = Column(String(20), nullable=False)
    s3_object_key = Column(Text)
    text_content = Column(Text(2000))  # テキストコンテンツを保存するカラム

    group_chat = relationship("GroupChat", back_populates="content")
