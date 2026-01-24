"""
SQLAlchemy database models
Defines all database tables for AI Studio
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Float,
)
from sqlalchemy.orm import relationship

from database.db import Base


class Chat(Base):
    """
    Chat sessions - represents a conversation
    """
    __tablename__ = "chats"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    folder_id = Column(Integer, ForeignKey("folders.id"), nullable=True)
    pinned = Column(Boolean, default=False)
    archived = Column(Boolean, default=False)
    tags = Column(Text, nullable=True)  # JSON array
    model_id = Column(Integer, ForeignKey("models.id"), nullable=True)
    
    # Relationships
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
    folder = relationship("Folder", back_populates="chats")
    model = relationship("Model", back_populates="chats")
    summaries = relationship("Summary", back_populates="chat", cascade="all, delete-orphan")


class Message(Base):
    """
    Individual messages within a chat
    """
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(20), nullable=False)  # 'user', 'assistant', 'system'
    content = Column(Text, nullable=False)
    thinking_content = Column(Text, nullable=True)  # For models with thinking capability
    tokens = Column(Integer, nullable=True)
    thinking_tokens = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    pinned = Column(Boolean, default=False)
    metadata = Column(Text, nullable=True)  # JSON: model used, settings, etc.
    
    # Relationships
    chat = relationship("Chat", back_populates="messages")


class SystemPrompt(Base):
    """
    Reusable system prompts library
    """
    __tablename__ = "system_prompts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    prompt = Column(Text, nullable=False)
    tags = Column(Text, nullable=True)  # JSON array
    icon = Column(String(50), nullable=True)
    usage_count = Column(Integer, default=0)
    default_settings = Column(Text, nullable=True)  # JSON
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Model(Base):
    """
    Model registry - local and API models
    """
    __tablename__ = "models"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    path = Column(Text, nullable=True)  # For local models
    type = Column(String(50), nullable=False)  # 'local', 'openai', 'anthropic', 'google', etc.
    size = Column(Integer, nullable=True)  # File size in bytes
    context_length = Column(Integer, nullable=True)
    parameters = Column(String(50), nullable=True)  # e.g., "7B", "13B"
    metadata = Column(Text, nullable=True)  # JSON: quantization, architecture, etc.
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    chats = relationship("Chat", back_populates="model")


class LoRA(Base):
    """
    LoRA adapters for local models
    """
    __tablename__ = "loras"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    path = Column(Text, nullable=False)
    compatible_models = Column(Text, nullable=True)  # JSON array of model IDs
    weight = Column(Float, default=1.0)
    enabled = Column(Boolean, default=True)
    metadata = Column(Text, nullable=True)  # JSON
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class KnowledgeSource(Base):
    """
    Documents and files added to knowledge base (RAG)
    """
    __tablename__ = "knowledge_sources"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)  # 'pdf', 'txt', 'docx', 'url', etc.
    path = Column(Text, nullable=True)
    chunk_count = Column(Integer, default=0)
    embedding_model = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    metadata = Column(Text, nullable=True)  # JSON: page count, file size, etc.


class Folder(Base):
    """
    Folders for organizing chats
    """
    __tablename__ = "folders"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    parent_id = Column(Integer, ForeignKey("folders.id"), nullable=True)
    icon = Column(String(50), nullable=True)
    color = Column(String(50), nullable=True)
    
    # Relationships
    chats = relationship("Chat", back_populates="folder")
    parent = relationship("Folder", remote_side=[id], backref="children")


class Setting(Base):
    """
    Application settings key-value store
    """
    __tablename__ = "settings"
    
    key = Column(String(255), primary_key=True)
    value = Column(Text, nullable=False)  # JSON
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Summary(Base):
    """
    Chat summaries for context management
    """
    __tablename__ = "summaries"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    summary = Column(Text, nullable=False)
    message_range = Column(Text, nullable=True)  # JSON: {start: msg_id, end: msg_id}
    tokens = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    chat = relationship("Chat", back_populates="summaries")
