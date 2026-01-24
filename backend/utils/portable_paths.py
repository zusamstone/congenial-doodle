"""
Portable paths management
Handles path resolution for portable application
"""
import os
from pathlib import Path
from typing import Optional

from loguru import logger

from utils.config import settings


def get_app_root() -> Path:
    """
    Get the application root directory
    In production: directory where executable is located
    In development: project root
    """
    # Check if running as packaged app
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return Path(sys.executable).parent
    else:
        # Running in development
        return Path(__file__).parent.parent


def get_data_dir() -> Path:
    """
    Get the data directory path
    This is where all user data, models, and databases are stored
    """
    data_dir = Path(settings.DATA_DIR)
    
    # Make absolute if relative
    if not data_dir.is_absolute():
        data_dir = get_app_root() / data_dir
    
    return data_dir


def get_models_dir() -> Path:
    """
    Get the models directory path
    """
    models_dir = Path(settings.MODELS_DIR)
    
    if not models_dir.is_absolute():
        models_dir = get_data_dir() / "models"
    
    return models_dir


def get_vector_store_dir() -> Path:
    """
    Get the vector store directory path (ChromaDB)
    """
    vector_dir = Path(settings.VECTOR_STORE_DIR)
    
    if not vector_dir.is_absolute():
        vector_dir = get_data_dir() / "vector_store"
    
    return vector_dir


def get_database_dir() -> Path:
    """
    Get the database directory path
    """
    db_dir = Path(settings.DATABASE_DIR)
    
    if not db_dir.is_absolute():
        db_dir = get_data_dir() / "database"
    
    return db_dir


def get_database_path() -> Path:
    """
    Get the full database file path
    """
    return get_database_dir() / settings.DATABASE_NAME


def get_uploads_dir() -> Path:
    """
    Get the uploads directory path
    """
    uploads_dir = Path(settings.UPLOADS_DIR)
    
    if not uploads_dir.is_absolute():
        uploads_dir = get_data_dir() / "uploads"
    
    return uploads_dir


def get_logs_dir() -> Path:
    """
    Get the logs directory path
    """
    logs_dir = get_data_dir() / "logs"
    return logs_dir


def ensure_directory(path: Path) -> None:
    """
    Ensure a directory exists, create if it doesn't
    """
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {path}")


def ensure_data_directories() -> None:
    """
    Ensure all required data directories exist
    Called during application startup
    """
    directories = [
        get_data_dir(),
        get_models_dir(),
        get_vector_store_dir(),
        get_database_dir(),
        get_uploads_dir(),
        get_logs_dir(),
    ]
    
    for directory in directories:
        ensure_directory(directory)
    
    logger.info("All data directories verified")


def get_model_path(model_filename: str) -> Path:
    """
    Get full path for a model file
    """
    return get_models_dir() / model_filename


def get_upload_path(filename: str) -> Path:
    """
    Get full path for an uploaded file
    """
    return get_uploads_dir() / filename


def is_portable_mode() -> bool:
    """
    Check if running in portable mode
    Portable mode: all data in ./data relative to executable
    """
    # If DATA_DIR is relative, we're in portable mode
    return not Path(settings.DATA_DIR).is_absolute()


# Import sys for frozen check
import sys
