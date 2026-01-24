"""
LoRA adapter management API routes
Handles loading and managing LoRA adapters for local models
"""
from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from loguru import logger

from database.db import get_db
from database.models import LoRA


router = APIRouter()


# Pydantic models
class LoRAResponse(BaseModel):
    """Response model for a LoRA adapter"""
    id: int
    name: str
    path: str
    compatible_models: Optional[List[int]] = None
    weight: float
    enabled: bool
    metadata: Optional[dict] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class LoRACreate(BaseModel):
    """Request model for creating a LoRA adapter"""
    name: str = Field(..., min_length=1)
    path: str = Field(..., min_length=1)
    compatible_models: Optional[List[int]] = None
    weight: float = Field(1.0, ge=0.0, le=2.0)
    metadata: Optional[dict] = None


class LoRAUpdate(BaseModel):
    """Request model for updating a LoRA adapter"""
    weight: Optional[float] = Field(None, ge=0.0, le=2.0)
    enabled: Optional[bool] = None


@router.get("/", response_model=List[LoRAResponse])
async def get_loras(
    model_id: Optional[int] = None,
    enabled_only: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all LoRA adapters
    Optionally filter by compatible model or enabled status
    """
    query = select(LoRA)
    
    if enabled_only:
        query = query.where(LoRA.enabled == True)
    
    result = await db.execute(query)
    loras = result.scalars().all()
    
    # Filter by model compatibility if specified
    if model_id is not None:
        loras = [
            lora for lora in loras
            if lora.compatible_models and model_id in lora.compatible_models
        ]
    
    return loras


@router.get("/{lora_id}", response_model=LoRAResponse)
async def get_lora(
    lora_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific LoRA adapter
    """
    result = await db.execute(select(LoRA).where(LoRA.id == lora_id))
    lora = result.scalar_one_or_none()
    
    if not lora:
        raise HTTPException(status_code=404, detail="LoRA adapter not found")
    
    return lora


@router.post("/", response_model=LoRAResponse)
async def create_lora(
    lora_data: LoRACreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new LoRA adapter
    """
    lora = LoRA(**lora_data.model_dump())
    
    db.add(lora)
    await db.commit()
    await db.refresh(lora)
    
    logger.info(f"Registered new LoRA: {lora.id} - {lora.name}")
    
    return lora


@router.patch("/{lora_id}", response_model=LoRAResponse)
async def update_lora(
    lora_id: int,
    lora_data: LoRAUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a LoRA adapter (weight or enabled status)
    """
    result = await db.execute(select(LoRA).where(LoRA.id == lora_id))
    lora = result.scalar_one_or_none()
    
    if not lora:
        raise HTTPException(status_code=404, detail="LoRA adapter not found")
    
    update_data = lora_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(lora, field, value)
    
    await db.commit()
    await db.refresh(lora)
    
    logger.info(f"Updated LoRA: {lora_id}")
    
    # TODO: If model is loaded with this LoRA, reload it with new settings
    
    return lora


@router.delete("/{lora_id}")
async def delete_lora(
    lora_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a LoRA adapter from registry
    Note: This does not delete the LoRA file
    """
    result = await db.execute(select(LoRA).where(LoRA.id == lora_id))
    lora = result.scalar_one_or_none()
    
    if not lora:
        raise HTTPException(status_code=404, detail="LoRA adapter not found")
    
    # TODO: Unload LoRA if currently applied to a loaded model
    
    await db.delete(lora)
    await db.commit()
    
    logger.info(f"Deleted LoRA: {lora_id}")
    
    return {"status": "deleted", "lora_id": lora_id}


@router.post("/{lora_id}/apply")
async def apply_lora(
    lora_id: int,
    model_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Apply a LoRA adapter to a loaded model
    TODO: Implement LoRA application
    """
    result = await db.execute(select(LoRA).where(LoRA.id == lora_id))
    lora = result.scalar_one_or_none()
    
    if not lora:
        raise HTTPException(status_code=404, detail="LoRA adapter not found")
    
    # TODO: Check if model is loaded
    # TODO: Check if LoRA is compatible with model
    # TODO: Apply LoRA to loaded model
    # TODO: Update model manager state
    
    logger.info(f"Applying LoRA {lora_id} to model {model_id}")
    
    raise HTTPException(
        status_code=501,
        detail="LoRA application not yet implemented"
    )


@router.post("/{lora_id}/remove")
async def remove_lora(
    lora_id: int,
    model_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Remove a LoRA adapter from a loaded model
    TODO: Implement LoRA removal
    """
    result = await db.execute(select(LoRA).where(LoRA.id == lora_id))
    lora = result.scalar_one_or_none()
    
    if not lora:
        raise HTTPException(status_code=404, detail="LoRA adapter not found")
    
    # TODO: Check if model is loaded
    # TODO: Check if LoRA is currently applied
    # TODO: Remove LoRA from loaded model
    # TODO: Update model manager state
    
    logger.info(f"Removing LoRA {lora_id} from model {model_id}")
    
    raise HTTPException(
        status_code=501,
        detail="LoRA removal not yet implemented"
    )
