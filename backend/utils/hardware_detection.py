"""
Hardware detection utilities
Detects CPU, GPU, and memory capabilities for optimal model loading
"""
import platform
from typing import Dict, List, Optional
from dataclasses import dataclass

import psutil
from loguru import logger


@dataclass
class CPUInfo:
    """CPU information"""
    cores_physical: int
    cores_logical: int
    frequency_max: float  # MHz
    frequency_current: float  # MHz
    architecture: str
    brand: str


@dataclass
class GPUInfo:
    """GPU information"""
    name: str
    vendor: str
    vram_total: int  # MB
    vram_free: int  # MB
    compute_capability: Optional[str] = None
    driver_version: Optional[str] = None


@dataclass
class MemoryInfo:
    """System memory information"""
    total: int  # MB
    available: int  # MB
    used: int  # MB
    percent_used: float


@dataclass
class HardwareInfo:
    """Complete hardware information"""
    cpu: CPUInfo
    gpu: Optional[List[GPUInfo]]
    memory: MemoryInfo
    platform: str
    has_cuda: bool
    has_metal: bool
    has_vulkan: bool


def get_cpu_info() -> CPUInfo:
    """
    Get CPU information
    """
    try:
        freq = psutil.cpu_freq()
        
        return CPUInfo(
            cores_physical=psutil.cpu_count(logical=False) or 1,
            cores_logical=psutil.cpu_count(logical=True) or 1,
            frequency_max=freq.max if freq else 0.0,
            frequency_current=freq.current if freq else 0.0,
            architecture=platform.machine(),
            brand=platform.processor() or "Unknown",
        )
    except Exception as e:
        logger.error(f"Error getting CPU info: {e}")
        return CPUInfo(
            cores_physical=1,
            cores_logical=1,
            frequency_max=0.0,
            frequency_current=0.0,
            architecture=platform.machine(),
            brand="Unknown",
        )


def get_gpu_info() -> Optional[List[GPUInfo]]:
    """
    Get GPU information
    TODO: Implement GPU detection for NVIDIA, AMD, Apple Silicon
    """
    gpus = []
    
    # Try NVIDIA
    try:
        import pynvml
        pynvml.nvmlInit()
        device_count = pynvml.nvmlDeviceGetCount()
        
        for i in range(device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            name = pynvml.nvmlDeviceGetName(handle)
            memory = pynvml.nvmlDeviceGetMemoryInfo(handle)
            
            gpus.append(GPUInfo(
                name=name.decode('utf-8') if isinstance(name, bytes) else name,
                vendor="NVIDIA",
                vram_total=memory.total // (1024 * 1024),
                vram_free=memory.free // (1024 * 1024),
                driver_version=pynvml.nvmlSystemGetDriverVersion().decode('utf-8'),
            ))
        
        pynvml.nvmlShutdown()
    except ImportError:
        logger.debug("pynvml not available - NVIDIA GPU detection skipped")
    except Exception as e:
        logger.debug(f"NVIDIA GPU detection failed: {e}")
    
    # TODO: Try AMD (ROCm)
    # TODO: Try Apple Metal
    # TODO: Try Intel GPU
    
    return gpus if gpus else None


def get_memory_info() -> MemoryInfo:
    """
    Get system memory information
    """
    try:
        mem = psutil.virtual_memory()
        
        return MemoryInfo(
            total=mem.total // (1024 * 1024),
            available=mem.available // (1024 * 1024),
            used=mem.used // (1024 * 1024),
            percent_used=mem.percent,
        )
    except Exception as e:
        logger.error(f"Error getting memory info: {e}")
        return MemoryInfo(
            total=0,
            available=0,
            used=0,
            percent_used=0.0,
        )


def has_cuda() -> bool:
    """
    Check if CUDA is available
    """
    try:
        import torch
        return torch.cuda.is_available()
    except ImportError:
        pass
    
    try:
        import pynvml
        pynvml.nvmlInit()
        device_count = pynvml.nvmlDeviceGetCount()
        pynvml.nvmlShutdown()
        return device_count > 0
    except:
        pass
    
    return False


def has_metal() -> bool:
    """
    Check if Metal (Apple Silicon) is available
    """
    if platform.system() != "Darwin":
        return False
    
    # Check for Apple Silicon
    machine = platform.machine()
    return machine in ["arm64", "aarch64"]


def has_vulkan() -> bool:
    """
    Check if Vulkan is available
    TODO: Implement Vulkan detection
    """
    # TODO: Check for Vulkan support
    return False


def get_hardware_info() -> HardwareInfo:
    """
    Get complete hardware information
    """
    return HardwareInfo(
        cpu=get_cpu_info(),
        gpu=get_gpu_info(),
        memory=get_memory_info(),
        platform=platform.system(),
        has_cuda=has_cuda(),
        has_metal=has_metal(),
        has_vulkan=has_vulkan(),
    )


def get_recommended_settings(hardware: Optional[HardwareInfo] = None) -> Dict:
    """
    Get recommended model loading settings based on hardware
    """
    if hardware is None:
        hardware = get_hardware_info()
    
    settings = {
        "threads": hardware.cpu.cores_physical,
        "gpu_layers": 0,
        "use_mmap": True,
        "use_mlock": False,
    }
    
    # If CUDA is available
    if hardware.has_cuda and hardware.gpu:
        gpu = hardware.gpu[0]  # Use first GPU
        
        # Estimate layers based on VRAM (rough estimate: 1GB per ~5 layers for 7B model)
        if gpu.vram_free > 8000:  # 8GB+
            settings["gpu_layers"] = 35  # Full offload for 7B
        elif gpu.vram_free > 4000:  # 4GB+
            settings["gpu_layers"] = 20  # Partial offload
        elif gpu.vram_free > 2000:  # 2GB+
            settings["gpu_layers"] = 10  # Minimal offload
        
        logger.info(f"CUDA available with {gpu.vram_free}MB VRAM - recommending {settings['gpu_layers']} GPU layers")
    
    # If Metal is available (Apple Silicon)
    elif hardware.has_metal:
        # Apple Silicon has unified memory, can offload more aggressively
        if hardware.memory.available > 16000:  # 16GB+
            settings["gpu_layers"] = 1  # Metal uses special value
        logger.info("Metal (Apple Silicon) detected - enabling GPU acceleration")
    
    # Adjust for low memory systems
    if hardware.memory.available < 4000:  # Less than 4GB available
        settings["use_mlock"] = False
        settings["threads"] = max(2, hardware.cpu.cores_physical // 2)
        logger.warning("Low memory detected - using conservative settings")
    
    return settings


def log_hardware_info():
    """
    Log hardware information for debugging
    """
    hardware = get_hardware_info()
    
    logger.info(f"Platform: {hardware.platform}")
    logger.info(f"CPU: {hardware.cpu.brand} ({hardware.cpu.cores_physical} cores, {hardware.cpu.cores_logical} threads)")
    logger.info(f"Memory: {hardware.memory.total}MB total, {hardware.memory.available}MB available")
    
    if hardware.gpu:
        for i, gpu in enumerate(hardware.gpu):
            logger.info(f"GPU {i}: {gpu.vendor} {gpu.name} ({gpu.vram_total}MB VRAM, {gpu.vram_free}MB free)")
    else:
        logger.info("GPU: None detected")
    
    logger.info(f"CUDA: {'Available' if hardware.has_cuda else 'Not available'}")
    logger.info(f"Metal: {'Available' if hardware.has_metal else 'Not available'}")
    logger.info(f"Vulkan: {'Available' if hardware.has_vulkan else 'Not available'}")
