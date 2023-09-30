import torch


def max_cuda_memory_allocated(device=None):
    r"""Returns the maximum GPU memory occupied by tensors in megabytes for a given device.

    Args:
        device (torch.device, optional): selected device. Defaults to current CUDA device.

    Returns:
        int: maximum GPU memory occupied by tensors in bytes for a given device.
    """
    if device is None:
        device = torch.cuda.current_device()
    return torch.cuda.max_memory_allocated(device) / 1024**2


def is_cuda_available():
    """Check if CUDA is available"""
    return torch.cuda.is_available()


def get_device():
    """Get current device"""
    DEVICE = 'cpu'
    if is_cuda_available():
        DEVICE = 'cuda'
    return DEVICE
