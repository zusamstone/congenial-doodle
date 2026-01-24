"""
Inference Engine for Local Model Execution using llama.cpp

This module provides a high-performance inference engine for running GGUF models
locally with GPU acceleration support (CUDA, Metal, Vulkan).
"""

import asyncio
import logging
from pathlib import Path
from typing import AsyncIterator, Dict, Any, Optional, List
from dataclasses import dataclass
import psutil

try:
    from llama_cpp import Llama
except ImportError:
    Llama = None
    logging.warning("llama-cpp-python not installed. Local inference will not be available.")


logger = logging.getLogger(__name__)


@dataclass
class InferenceConfig:
    """Configuration for inference engine."""
    model_path: str
    n_gpu_layers: int = -1  # -1 means use all available
    n_ctx: int = 4096
    n_threads: Optional[int] = None  # None = auto-detect
    n_batch: int = 512
    rope_scaling_type: Optional[int] = None
    rope_freq_base: Optional[float] = None
    rope_freq_scale: Optional[float] = None
    use_mmap: bool = True
    use_mlock: bool = False
    verbose: bool = False


@dataclass
class SamplingParams:
    """Sampling parameters for text generation."""
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 40
    repeat_penalty: float = 1.1
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    max_tokens: int = 2048
    stop_sequences: List[str] = None
    seed: Optional[int] = None
    # Advanced sampling
    mirostat: int = 0
    mirostat_tau: float = 5.0
    mirostat_eta: float = 0.1
    tfs_z: float = 1.0
    typical_p: float = 1.0
    min_p: float = 0.05

    def __post_init__(self):
        if self.stop_sequences is None:
            self.stop_sequences = []


class InferenceEngine:
    """
    High-performance inference engine for local GGUF models.
    
    Features:
    - Automatic GPU detection and layer offloading
    - Streaming token generation
    - Advanced sampling parameters
    - Memory-efficient model loading
    - Thread count optimization
    
    Example:
        ```python
        engine = InferenceEngine(
            model_path="/path/to/model.gguf",
            n_gpu_layers=-1  # Use all GPU layers
        )
        
        # Streaming generation
        async for token in engine.generate_stream(
            prompt="Once upon a time",
            temperature=0.7,
            max_tokens=100
        ):
            print(token, end='', flush=True)
        ```
    """

    def __init__(self, config: InferenceConfig):
        """
        Initialize the inference engine.
        
        Args:
            config: Configuration for the inference engine
            
        Raises:
            ImportError: If llama-cpp-python is not installed
            FileNotFoundError: If model file doesn't exist
        """
        if Llama is None:
            raise ImportError(
                "llama-cpp-python is required for local inference. "
                "Install it with: pip install llama-cpp-python"
            )
        
        self.config = config
        self.model: Optional[Llama] = None
        self.loaded = False
        
        # Auto-detect thread count if not specified
        if self.config.n_threads is None:
            # Use physical cores, not logical (no hyperthreading)
            self.config.n_threads = psutil.cpu_count(logical=False) or 4
        
        # Validate model path
        if not Path(config.model_path).exists():
            raise FileNotFoundError(f"Model file not found: {config.model_path}")
        
        logger.info(f"Initializing inference engine for {config.model_path}")
        logger.info(f"GPU layers: {config.n_gpu_layers}, Threads: {config.n_threads}, Context: {config.n_ctx}")

    def load(self) -> None:
        """
        Load the model into memory.
        
        Raises:
            Exception: If model loading fails
        """
        if self.loaded:
            logger.warning("Model already loaded")
            return
        
        try:
            logger.info("Loading model...")
            
            # Build llama.cpp kwargs
            kwargs = {
                "model_path": self.config.model_path,
                "n_gpu_layers": self.config.n_gpu_layers,
                "n_ctx": self.config.n_ctx,
                "n_threads": self.config.n_threads,
                "n_batch": self.config.n_batch,
                "use_mmap": self.config.use_mmap,
                "use_mlock": self.config.use_mlock,
                "verbose": self.config.verbose,
            }
            
            # Add RoPE scaling if specified
            if self.config.rope_scaling_type is not None:
                kwargs["rope_scaling_type"] = self.config.rope_scaling_type
            if self.config.rope_freq_base is not None:
                kwargs["rope_freq_base"] = self.config.rope_freq_base
            if self.config.rope_freq_scale is not None:
                kwargs["rope_freq_scale"] = self.config.rope_freq_scale
            
            self.model = Llama(**kwargs)
            self.loaded = True
            
            logger.info("Model loaded successfully")
            
            # Log memory usage
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            logger.info(f"Memory usage: {memory_mb:.2f} MB")
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

    def unload(self) -> None:
        """Unload the model from memory."""
        if self.model is not None:
            logger.info("Unloading model...")
            del self.model
            self.model = None
            self.loaded = False
            
            # Force garbage collection
            import gc
            gc.collect()
            
            logger.info("Model unloaded")

    def generate(
        self,
        prompt: str,
        params: Optional[SamplingParams] = None
    ) -> str:
        """
        Generate text completion (non-streaming).
        
        Args:
            prompt: Input prompt
            params: Sampling parameters
            
        Returns:
            Generated text
            
        Raises:
            RuntimeError: If model is not loaded
        """
        if not self.loaded or self.model is None:
            raise RuntimeError("Model not loaded. Call load() first.")
        
        if params is None:
            params = SamplingParams()
        
        # Build generation kwargs
        kwargs = self._build_generation_kwargs(params)
        
        # Generate
        result = self.model(prompt, **kwargs)
        
        # Extract generated text
        if isinstance(result, dict) and "choices" in result:
            return result["choices"][0]["text"]
        return str(result)

    async def generate_stream(
        self,
        prompt: str,
        params: Optional[SamplingParams] = None
    ) -> AsyncIterator[str]:
        """
        Generate text completion with streaming.
        
        Args:
            prompt: Input prompt
            params: Sampling parameters
            
        Yields:
            Generated tokens as they are produced
            
        Raises:
            RuntimeError: If model is not loaded
        """
        if not self.loaded or self.model is None:
            raise RuntimeError("Model not loaded. Call load() first.")
        
        if params is None:
            params = SamplingParams()
        
        # Build generation kwargs
        kwargs = self._build_generation_kwargs(params)
        kwargs["stream"] = True
        
        # Generate in thread pool to avoid blocking event loop
        loop = asyncio.get_event_loop()
        
        def _generate():
            return self.model(prompt, **kwargs)
        
        # Run in executor
        generator = await loop.run_in_executor(None, _generate)
        
        # Stream tokens
        for chunk in generator:
            if isinstance(chunk, dict) and "choices" in chunk:
                text = chunk["choices"][0].get("text", "")
                if text:
                    yield text
                    # Small delay to allow other tasks
                    await asyncio.sleep(0)

    def _build_generation_kwargs(self, params: SamplingParams) -> Dict[str, Any]:
        """Build kwargs dict for llama.cpp generation."""
        kwargs = {
            "max_tokens": params.max_tokens,
            "temperature": params.temperature,
            "top_p": params.top_p,
            "top_k": params.top_k,
            "repeat_penalty": params.repeat_penalty,
            "frequency_penalty": params.frequency_penalty,
            "presence_penalty": params.presence_penalty,
        }
        
        # Add stop sequences
        if params.stop_sequences:
            kwargs["stop"] = params.stop_sequences
        
        # Add seed if specified
        if params.seed is not None:
            kwargs["seed"] = params.seed
        
        # Advanced sampling parameters
        if params.mirostat > 0:
            kwargs["mirostat_mode"] = params.mirostat
            kwargs["mirostat_tau"] = params.mirostat_tau
            kwargs["mirostat_eta"] = params.mirostat_eta
        
        if params.tfs_z < 1.0:
            kwargs["tfs_z"] = params.tfs_z
        
        if params.typical_p < 1.0:
            kwargs["typical_p"] = params.typical_p
        
        if params.min_p > 0.0:
            kwargs["min_p"] = params.min_p
        
        return kwargs

    def get_context_length(self) -> int:
        """Get the context length of the loaded model."""
        if not self.loaded or self.model is None:
            return 0
        return self.model.n_ctx()

    def get_vocab_size(self) -> int:
        """Get the vocabulary size of the loaded model."""
        if not self.loaded or self.model is None:
            return 0
        return self.model.n_vocab()

    def reset(self) -> None:
        """Reset the model state (clear KV cache)."""
        if self.loaded and self.model is not None:
            self.model.reset()
            logger.info("Model state reset")

    def __enter__(self):
        """Context manager entry."""
        if not self.loaded:
            self.load()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.unload()

    def __repr__(self) -> str:
        """String representation."""
        status = "loaded" if self.loaded else "not loaded"
        return f"InferenceEngine(model={Path(self.config.model_path).name}, status={status})"


# Convenience function for quick inference
async def quick_inference(
    model_path: str,
    prompt: str,
    max_tokens: int = 100,
    temperature: float = 0.7,
    n_gpu_layers: int = -1
) -> str:
    """
    Quick one-off inference without managing engine lifecycle.
    
    Args:
        model_path: Path to GGUF model file
        prompt: Input prompt
        max_tokens: Maximum tokens to generate
        temperature: Sampling temperature
        n_gpu_layers: Number of layers to offload to GPU
        
    Returns:
        Generated text
    """
    config = InferenceConfig(
        model_path=model_path,
        n_gpu_layers=n_gpu_layers
    )
    
    params = SamplingParams(
        max_tokens=max_tokens,
        temperature=temperature
    )
    
    with InferenceEngine(config) as engine:
        return engine.generate(prompt, params)
