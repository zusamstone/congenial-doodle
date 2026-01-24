"""
Chat API routes
Handles chat sessions, messages, and streaming
"""
from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from pydantic import BaseModel, Field
from loguru import logger

from database.db import get_db
from database.models import Chat, Message


router = APIRouter()


# Pydantic models for request/response validation
class MessageCreate(BaseModel):
    """Request model for creating a message"""
    chat_id: Optional[int] = None
    message: str = Field(..., min_length=1)
    model_id: Optional[int] = None
    system_prompt_id: Optional[int] = None
    settings: Optional[dict] = None


class MessageResponse(BaseModel):
    """Response model for a message"""
    id: int
    chat_id: int
    role: str
    content: str
    thinking_content: Optional[str] = None
    tokens: Optional[int] = None
    thinking_tokens: Optional[int] = None
    created_at: datetime
    pinned: bool
    metadata: Optional[dict] = None
    
    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    """Response model for a chat"""
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    folder_id: Optional[int] = None
    pinned: bool
    archived: bool
    tags: Optional[List[str]] = None
    model_id: Optional[int] = None
    message_count: Optional[int] = None
    
    class Config:
        from_attributes = True


@router.post("/send", response_model=MessageResponse)
async def send_message(
    message_data: MessageCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Send a message and get a response
    TODO: Implement actual AI inference
    TODO: Handle streaming via WebSocket instead
    """
    # TODO: Load model
    # TODO: Get system prompt if specified
    # TODO: Retrieve chat history
    # TODO: Apply RAG if enabled
    # TODO: Generate response
    # TODO: Save message and response
    
    raise HTTPException(
        status_code=501,
        detail="Not implemented - use WebSocket endpoint for chat"
    )


@router.get("/{chat_id}/messages", response_model=List[MessageResponse])
async def get_chat_messages(
    chat_id: int,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all messages in a chat
    """
    # Verify chat exists
    result = await db.execute(select(Chat).where(Chat.id == chat_id))
    chat = result.scalar_one_or_none()
    
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    # Get messages
    result = await db.execute(
        select(Message)
        .where(Message.chat_id == chat_id)
        .order_by(Message.created_at)
        .limit(limit)
        .offset(offset)
    )
    messages = result.scalars().all()
    
    return messages


@router.get("/", response_model=List[ChatResponse])
async def get_chats(
    folder_id: Optional[int] = None,
    archived: bool = False,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all chats, optionally filtered by folder
    """
    query = select(Chat).where(Chat.archived == archived)
    
    if folder_id is not None:
        query = query.where(Chat.folder_id == folder_id)
    
    query = query.order_by(desc(Chat.updated_at)).limit(limit).offset(offset)
    
    result = await db.execute(query)
    chats = result.scalars().all()
    
    return chats


@router.post("/", response_model=ChatResponse)
async def create_chat(
    title: str = "New Chat",
    model_id: Optional[int] = None,
    folder_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new chat session
    """
    chat = Chat(
        title=title,
        model_id=model_id,
        folder_id=folder_id,
    )
    
    db.add(chat)
    await db.commit()
    await db.refresh(chat)
    
    logger.info(f"Created new chat: {chat.id} - {chat.title}")
    
    return chat


@router.delete("/{chat_id}")
async def delete_chat(
    chat_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a chat and all its messages
    """
    result = await db.execute(select(Chat).where(Chat.id == chat_id))
    chat = result.scalar_one_or_none()
    
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    await db.delete(chat)
    await db.commit()
    
    logger.info(f"Deleted chat: {chat_id}")
    
    return {"status": "deleted", "chat_id": chat_id}


@router.patch("/{chat_id}/message/{message_id}", response_model=MessageResponse)
async def edit_message(
    chat_id: int,
    message_id: int,
    content: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Edit a message (typically user messages)
    TODO: Implement regeneration after edit
    """
    result = await db.execute(
        select(Message).where(
            Message.id == message_id,
            Message.chat_id == chat_id
        )
    )
    message = result.scalar_one_or_none()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.content = content
    await db.commit()
    await db.refresh(message)
    
    logger.info(f"Edited message: {message_id}")
    
    return message


@router.websocket("/stream")
async def websocket_chat(websocket: WebSocket):
    """
    WebSocket endpoint for streaming chat responses
    TODO: Implement full streaming logic
    """
    await websocket.accept()
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            
            # TODO: Validate data
            # TODO: Load model
            # TODO: Get chat history
            # TODO: Apply system prompt
            # TODO: Apply RAG if enabled
            # TODO: Generate response with streaming
            # TODO: Save messages to database
            
            # Placeholder response
            await websocket.send_json({
                "type": "error",
                "error": "Streaming not yet implemented",
            })
            
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close(code=1011, reason=str(e))
