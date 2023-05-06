from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.cruds.user import get_user2

# schema
import app.schemas.group as group_schema
import app.schemas.group_chat as group_chat_schema

import app.schemas.user as user_schema
# model
import app.models.group as group_model
import app.models.user as user_model

import app.models.group_chat as group_chat_model


# traceback
import traceback

from typing import List, Tuple, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.engine import Result

    
#  post create_group_chat_content
async def create_group_chat_content(db: AsyncSession, content: group_chat_schema.GroupChatContentCreate):
    async with db.begin():
        group_chat = group_chat_model.GroupChat(group_id=content.group_id, user_id=content.user_id)
        db.add(group_chat)
        await db.flush()

        group_chat_content = group_chat_model.GroupChatContent(
            group_chat_id=group_chat.id,
            content_type=content.content_type,
            s3_object_key=content.s3_object_key,
            text_content=content.text_content
        )
        db.add(group_chat_content)
        await db.flush()

    await db.refresh(group_chat_content)
    await db.refresh(group_chat, options=[selectinload(group_chat_model.GroupChat.content)])

    return group_chat_content

