"""
Configuration management
Loads settings from environment variables and config files
"""
import os
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger


class Settings(BaseSettings):
    """
    Application settings
    Loads from environment variables and .env file
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    # Application
    APP_NAME: str = "AI Studio"
    VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # Server
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    # Paths (portable mode)
    DATA_DIR: str = "./data"
    MODELS_DIR: str = "./data/models"
    VECTOR_STORE_DIR: str = "./data/vector_store"
    DATABASE_DIR: str = "./data/database"
    UPLOADS_DIR: str = "./data/uploads"
    
    # Database
    DATABASE_NAME: str = "ai_studio.db"
    
    # Models
    DEFAULT_MODEL: Optional[str] = None
    DEFAULT_EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Hardware
    DEFAULT_GPU_LAYERS: int = 0  # 0 = CPU only
    DEFAULT_THREADS: int = 4
    
    # Context
    DEFAULT_CONTEXT_LENGTH: int = 4096
    MAX_CONTEXT_LENGTH: int = 32768
    
    # RAG
    DEFAULT_CHUNK_SIZE: int = 512
    DEFAULT_CHUNK_OVERLAP: int = 50
    DEFAULT_MAX_CHUNKS: int = 5
    DEFAULT_MIN_RELEVANCE: float = 0.5
    
    # API Keys (encrypted in database)
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    
    # Security
    ENCRYPTION_KEY: Optional[str] = None  # For encrypting API keys
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = "./data/logs/ai_studio.log"


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """
    Dependency to get settings instance
    """
    return settings


def load_config(config_path: Optional[Path] = None) -> dict:
    """
    Load configuration from JSON/YAML config file
    TODO: Implement config file loading
    """
    if config_path is None:
        config_path = Path("./config/settings.json")
    
    if not config_path.exists():
        logger.warning(f"Config file not found: {config_path}")
        return {}
    
    # TODO: Load and parse config file
    # TODO: Merge with environment variables
    # TODO: Validate configuration
    
    return {}


def save_config(config: dict, config_path: Optional[Path] = None) -> None:
    """
    Save configuration to file
    TODO: Implement config file saving
    """
    if config_path is None:
        config_path = Path("./config/settings.json")
    
    # TODO: Validate config
    # TODO: Write to file
    # TODO: Create backup
    
    pass


# Configure logging
logger.add(
    settings.LOG_FILE if settings.LOG_FILE else "ai_studio.log",
    rotation="10 MB",
    retention="7 days",
    level=settings.LOG_LEVEL,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
)
