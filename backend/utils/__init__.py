"""
Utilities package initialization
"""
from utils.config import settings, get_settings
from utils.portable_paths import (
    get_data_dir,
    get_models_dir,
    get_vector_store_dir,
    get_database_dir,
    get_database_path,
    get_uploads_dir,
    ensure_data_directories,
    is_portable_mode,
)
from utils.hardware_detection import (
    get_hardware_info,
    get_recommended_settings,
    log_hardware_info,
)

__all__ = [
    "settings",
    "get_settings",
    "get_data_dir",
    "get_models_dir",
    "get_vector_store_dir",
    "get_database_dir",
    "get_database_path",
    "get_uploads_dir",
    "ensure_data_directories",
    "is_portable_mode",
    "get_hardware_info",
    "get_recommended_settings",
    "log_hardware_info",
]
