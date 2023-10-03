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

def human_bytes(B):
    """
    Return the given bytes as a human friendly KB, MB, GB, or TB string
    """
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2)  # 1,048,576
    GB = float(KB ** 3)  # 1,073,741,824
    TB = float(KB ** 4)  # 1,099,511,627,776

    if B < KB:
        return "{0} {1}".format(B, "Bytes" if 0 == B > 1 else "Byte")
    elif KB <= B < MB:
        return "{0:.2f} KB".format(B / KB)
    elif MB <= B < GB:
        return "{0:.2f} MB".format(B / MB)
    elif GB <= B < TB:
        return "{0:.2f} GB".format(B / GB)
    elif TB <= B:
        return "{0:.2f} TB".format(B / TB)
