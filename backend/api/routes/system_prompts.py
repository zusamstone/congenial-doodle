"""
System prompts API routes
Handles system prompt library management
"""
from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from pydantic import BaseModel, Field
from loguru import logger

from database.db import get_db
from database.models import SystemPrompt


router = APIRouter()


# Pydantic models
class SystemPromptResponse(BaseModel):
    """Response model for a system prompt"""
    id: int
    name: str
    description: Optional[str] = None
    prompt: str
    tags: Optional[List[str]] = None
    icon: Optional[str] = None
    usage_count: int
    default_settings: Optional[dict] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SystemPromptCreate(BaseModel):
    """Request model for creating a system prompt"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    prompt: str = Field(..., min_length=1)
    tags: Optional[List[str]] = None
    icon: Optional[str] = None
    default_settings: Optional[dict] = None


class SystemPromptUpdate(BaseModel):
    """Request model for updating a system prompt"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    prompt: Optional[str] = Field(None, min_length=1)
    tags: Optional[List[str]] = None
    icon: Optional[str] = None
    default_settings: Optional[dict] = None


@router.get("/", response_model=List[SystemPromptResponse])
async def get_system_prompts(
    tag: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all system prompts
    Optionally filter by tag or search term
    """
    query = select(SystemPrompt)
    
    # TODO: Implement tag filtering (requires JSON query)
    # TODO: Implement search (name or description)
    
    query = query.order_by(desc(SystemPrompt.usage_count)).limit(limit).offset(offset)
    
    result = await db.execute(query)
    prompts = result.scalars().all()
    
    return prompts


@router.get("/{prompt_id}", response_model=SystemPromptResponse)
async def get_system_prompt(
    prompt_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific system prompt
    """
    result = await db.execute(
        select(SystemPrompt).where(SystemPrompt.id == prompt_id)
    )
    prompt = result.scalar_one_or_none()
    
    if not prompt:
        raise HTTPException(status_code=404, detail="System prompt not found")
    
    return prompt


@router.post("/", response_model=SystemPromptResponse)
async def create_system_prompt(
    prompt_data: SystemPromptCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new system prompt
    """
    # Check if name already exists
    result = await db.execute(
        select(SystemPrompt).where(SystemPrompt.name == prompt_data.name)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"System prompt with name '{prompt_data.name}' already exists"
        )
    
    prompt = SystemPrompt(**prompt_data.model_dump())
    
    db.add(prompt)
    await db.commit()
    await db.refresh(prompt)
    
    logger.info(f"Created system prompt: {prompt.id} - {prompt.name}")
    
    return prompt


@router.put("/{prompt_id}", response_model=SystemPromptResponse)
async def update_system_prompt(
    prompt_id: int,
    prompt_data: SystemPromptUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a system prompt
    """
    result = await db.execute(
        select(SystemPrompt).where(SystemPrompt.id == prompt_id)
    )
    prompt = result.scalar_one_or_none()
    
    if not prompt:
        raise HTTPException(status_code=404, detail="System prompt not found")
    
    # Check name uniqueness if name is being changed
    update_data = prompt_data.model_dump(exclude_unset=True)
    if "name" in update_data and update_data["name"] != prompt.name:
        result = await db.execute(
            select(SystemPrompt).where(SystemPrompt.name == update_data["name"])
        )
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"System prompt with name '{update_data['name']}' already exists"
            )
    
    for field, value in update_data.items():
        setattr(prompt, field, value)
    
    prompt.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(prompt)
    
    logger.info(f"Updated system prompt: {prompt_id}")
    
    return prompt


@router.delete("/{prompt_id}")
async def delete_system_prompt(
    prompt_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a system prompt
    """
    result = await db.execute(
        select(SystemPrompt).where(SystemPrompt.id == prompt_id)
    )
    prompt = result.scalar_one_or_none()
    
    if not prompt:
        raise HTTPException(status_code=404, detail="System prompt not found")
    
    await db.delete(prompt)
    await db.commit()
    
    logger.info(f"Deleted system prompt: {prompt_id}")
    
    return {"status": "deleted", "prompt_id": prompt_id}


@router.post("/{prompt_id}/use")
async def increment_usage(
    prompt_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Increment usage count for a system prompt
    Called when a prompt is used in a chat
    """
    result = await db.execute(
        select(SystemPrompt).where(SystemPrompt.id == prompt_id)
    )
    prompt = result.scalar_one_or_none()
    
    if not prompt:
        raise HTTPException(status_code=404, detail="System prompt not found")
    
    prompt.usage_count += 1
    
    await db.commit()
    await db.refresh(prompt)
    
    return {"status": "incremented", "usage_count": prompt.usage_count}
