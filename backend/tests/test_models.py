"""
Tests for inference engine and model management.
"""

import pytest
from pathlib import Path
from backend.models.inference_engine import InferenceConfig, SamplingParams
from backend.models.model_manager import ModelManager
from backend.models.api_providers import APIProviderConfig


def test_inference_config_creation():
    """Test InferenceConfig creation."""
    config = InferenceConfig(
        model_path="/path/to/model.gguf",
        n_gpu_layers=32,
        n_ctx=2048
    )
    
    assert config.model_path == "/path/to/model.gguf"
    assert config.n_gpu_layers == 32
    assert config.n_ctx == 2048
    assert config.n_threads is None  # Auto-detect


def test_sampling_params_defaults():
    """Test SamplingParams default values."""
    params = SamplingParams()
    
    assert params.temperature == 0.7
    assert params.top_p == 0.9
    assert params.top_k == 40
    assert params.max_tokens == 2048
    assert params.stop_sequences == []


def test_sampling_params_custom():
    """Test SamplingParams with custom values."""
    params = SamplingParams(
        temperature=0.9,
        max_tokens=100,
        stop_sequences=["</s>", "\n\n"]
    )
    
    assert params.temperature == 0.9
    assert params.max_tokens == 100
    assert len(params.stop_sequences) == 2


def test_model_manager_initialization():
    """Test ModelManager initialization."""
    manager = ModelManager(max_loaded=2)
    
    assert manager.max_loaded == 2
    assert len(manager.models) == 0
    assert len(manager.configs) == 0


def test_model_manager_registration():
    """Test model registration."""
    manager = ModelManager()
    
    config = InferenceConfig(
        model_path="/path/to/model.gguf",
        n_gpu_layers=-1
    )
    
    manager.register_model(
        model_id="test-model",
        config=config,
        metadata={"name": "Test Model", "size": "7B"}
    )
    
    assert "test-model" in manager.model_registry
    assert manager.model_registry["test-model"]["loaded"] is False
    assert manager.model_registry["test-model"]["metadata"]["name"] == "Test Model"


def test_model_manager_info():
    """Test getting model info."""
    manager = ModelManager()
    
    config = InferenceConfig(model_path="/path/to/model.gguf")
    manager.register_model("test-model", config)
    
    info = manager.get_model_info("test-model")
    assert info is not None
    assert info["model_id"] == "test-model"
    assert info["loaded"] is False


def test_model_manager_memory_usage():
    """Test memory usage reporting."""
    manager = ModelManager()
    usage = manager.get_memory_usage()
    
    assert "process_rss_mb" in usage
    assert "system_total_mb" in usage
    assert "system_percent" in usage
    assert usage["system_percent"] >= 0


def test_api_provider_config():
    """Test APIProviderConfig creation."""
    config = APIProviderConfig(
        api_key="test-key",
        base_url="https://api.example.com",
        timeout=30
    )
    
    assert config.api_key == "test-key"
    assert config.base_url == "https://api.example.com"
    assert config.timeout == 30


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
