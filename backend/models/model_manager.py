"""
Model Manager for handling multiple models and their lifecycle.

This module provides centralized model management including:
- Loading/unloading models
- Model registry
- VRAM tracking
- LRU cache for automatic unloading
"""

import logging
from typing import Dict, Optional, List
from datetime import datetime
from collections import OrderedDict
import psutil

from .inference_engine import InferenceEngine, InferenceConfig


logger = logging.getLogger(__name__)


class ModelManager:
    """
    Manages multiple inference engines with automatic resource management.
    
    Features:
    - Lazy loading (load on first use)
    - LRU cache with automatic unloading
    - VRAM tracking
    - Model registry
    
    Example:
        ```python
        manager = ModelManager(max_loaded=3)
        
        # Load a model (lazy)
        engine = await manager.get_model("llama-7b")
        
        # Generate
        async for token in engine.generate_stream("Hello"):
            print(token, end='')
        ```
    """

    def __init__(self, max_loaded: int = 3):
        """
        Initialize the model manager.
        
        Args:
            max_loaded: Maximum number of models to keep loaded simultaneously
        """
        self.max_loaded = max_loaded
        self.models: Dict[str, InferenceEngine] = {}
        self.configs: Dict[str, InferenceConfig] = {}
        self.lru_order: OrderedDict[str, datetime] = OrderedDict()
        self.model_registry: Dict[str, Dict] = {}
        
        logger.info(f"ModelManager initialized (max_loaded={max_loaded})")

    def register_model(
        self,
        model_id: str,
        config: InferenceConfig,
        metadata: Optional[Dict] = None
    ) -> None:
        """
        Register a model with the manager.
        
        Args:
            model_id: Unique identifier for the model
            config: Inference configuration
            metadata: Optional metadata (name, size, etc.)
        """
        self.configs[model_id] = config
        self.model_registry[model_id] = {
            "model_id": model_id,
            "config": config,
            "metadata": metadata or {},
            "loaded": False,
            "last_used": None
        }
        
        logger.info(f"Registered model: {model_id}")

    async def get_model(self, model_id: str) -> InferenceEngine:
        """
        Get a model engine, loading it if necessary.
        
        Args:
            model_id: Model identifier
            
        Returns:
            Loaded inference engine
            
        Raises:
            KeyError: If model not registered
        """
        if model_id not in self.configs:
            raise KeyError(f"Model not registered: {model_id}")
        
        # Check if already loaded
        if model_id in self.models:
            # Update LRU order
            self.lru_order.move_to_end(model_id)
            self.lru_order[model_id] = datetime.now()
            logger.debug(f"Using cached model: {model_id}")
            return self.models[model_id]
        
        # Need to load - check if we need to unload something first
        if len(self.models) >= self.max_loaded:
            await self._unload_lru()
        
        # Load the model
        logger.info(f"Loading model: {model_id}")
        engine = InferenceEngine(self.configs[model_id])
        engine.load()
        
        # Add to cache
        self.models[model_id] = engine
        self.lru_order[model_id] = datetime.now()
        self.model_registry[model_id]["loaded"] = True
        self.model_registry[model_id]["last_used"] = datetime.now()
        
        return engine

    async def unload_model(self, model_id: str) -> None:
        """
        Unload a specific model.
        
        Args:
            model_id: Model to unload
        """
        if model_id not in self.models:
            logger.warning(f"Model not loaded: {model_id}")
            return
        
        logger.info(f"Unloading model: {model_id}")
        self.models[model_id].unload()
        del self.models[model_id]
        
        if model_id in self.lru_order:
            del self.lru_order[model_id]
        
        self.model_registry[model_id]["loaded"] = False

    async def _unload_lru(self) -> None:
        """Unload the least recently used model."""
        if not self.lru_order:
            return
        
        # Get least recently used
        lru_model_id = next(iter(self.lru_order))
        logger.info(f"Unloading LRU model: {lru_model_id}")
        await self.unload_model(lru_model_id)

    def unload_all(self) -> None:
        """Unload all models."""
        logger.info("Unloading all models...")
        for model_id in list(self.models.keys()):
            self.models[model_id].unload()
            del self.models[model_id]
        
        self.lru_order.clear()
        
        for model_id in self.model_registry:
            self.model_registry[model_id]["loaded"] = False
        
        logger.info("All models unloaded")

    def get_loaded_models(self) -> List[str]:
        """Get list of currently loaded model IDs."""
        return list(self.models.keys())

    def get_registry(self) -> Dict[str, Dict]:
        """Get the full model registry."""
        return self.model_registry.copy()

    def get_memory_usage(self) -> Dict[str, float]:
        """
        Get current memory usage.
        
        Returns:
            Dict with RAM and process memory in MB
        """
        process = psutil.Process()
        memory_info = process.memory_info()
        
        vm = psutil.virtual_memory()
        
        return {
            "process_rss_mb": memory_info.rss / 1024 / 1024,
            "process_vms_mb": memory_info.vms / 1024 / 1024,
            "system_total_mb": vm.total / 1024 / 1024,
            "system_used_mb": vm.used / 1024 / 1024,
            "system_available_mb": vm.available / 1024 / 1024,
            "system_percent": vm.percent
        }

    def get_model_info(self, model_id: str) -> Optional[Dict]:
        """
        Get information about a specific model.
        
        Args:
            model_id: Model identifier
            
        Returns:
            Model info dict or None if not found
        """
        return self.model_registry.get(model_id)

    def is_loaded(self, model_id: str) -> bool:
        """Check if a model is currently loaded."""
        return model_id in self.models

    def __repr__(self) -> str:
        """String representation."""
        loaded = len(self.models)
        registered = len(self.model_registry)
        return f"ModelManager(loaded={loaded}/{self.max_loaded}, registered={registered})"
