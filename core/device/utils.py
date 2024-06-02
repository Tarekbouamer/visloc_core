import random
import numpy as np
import torch

try:
    from loguru import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')


def max_cuda_memory_allocated(device=None):
    """Returns the maximum memory allocated on the current or specified CUDA device in megabytes."""
    if device is None:
        device = torch.cuda.current_device()
    return torch.cuda.max_memory_allocated(device) / 1024**2


def is_cuda_available():
    """Returns True if CUDA is available, otherwise False."""
    return torch.cuda.is_available()


def get_device():
    """Returns 'cuda' if CUDA is available, otherwise returns 'cpu'. Uses memoization to store the device."""
    if not hasattr(get_device, "DEVICE"):
        get_device.DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    return get_device.DEVICE


def human_bytes(B):
    """Converts bytes to a human-readable format (KB, MB, GB, TB)."""
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2)
    GB = float(KB ** 3)
    TB = float(KB ** 4)

    if B < KB:
        return f"{B} {'Bytes' if B == 0 or B > 1 else 'Byte'}"
    elif KB <= B < MB:
        return f"{B / KB:.2f} KB"
    elif MB <= B < GB:
        return f"{B / MB:.2f} MB"
    elif GB <= B < TB:
        return f"{B / GB:.2f} GB"
    else:
        return f"{B / TB:.2f} TB"


def random_seed(seed=42, rank=0):
    """Sets the seed for random number generators in numpy, random, and torch for reproducibility."""
    torch.manual_seed(seed + rank)
    np.random.seed(seed + rank)
    random.seed(seed + rank)


def print_cuda_memory_usage():
    """Logs the current CUDA memory usage including total, allocated, and cached memory."""
    logger.info(
        f"Total memory: {torch.cuda.get_device_properties(0).total_memory / 1024**2:.2f} MB")
    logger.info(
        f"Allocated memory: {torch.cuda.memory_allocated() / 1024**2:.2f} MB")
    logger.info(
        f"Cached memory: {torch.cuda.memory_reserved() / 1024**2:.2f} MB")


def set_cuda_device(device_id):
    """Sets the specified device as the current CUDA device and logs the change."""
    torch.cuda.set_device(device_id)
    logger.info(f"Current CUDA Device: GPU {torch.cuda.current_device()}")


def enhanced_random_seed(seed=42, rank=0, use_cuda=False):
    """Enhanced random seeding which also seeds all CUDA devices if CUDA is available and requested."""
    random_seed(seed, rank)
    if use_cuda and torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed + rank)


def clear_cuda_cache():
    """Clears the CUDA memory cache and logs this action."""
    torch.cuda.empty_cache()
    logger.info("CUDA cache cleared.")


def set_benchmark_mode(status=True):
    """Enables or disables the benchmark mode in torch based on the provided status."""
    torch.backends.cudnn.benchmark = status
