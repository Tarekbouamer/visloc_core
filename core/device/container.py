import torch


def to_cpu(data):
    """Move data to CPU"""
    if isinstance(data, dict):
        return {k: to_cpu(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [to_cpu(v) for v in data]
    elif isinstance(data, tuple):
        return tuple(to_cpu(v) for v in data)
    elif isinstance(data, set):
        return {to_cpu(v) for v in data}
    elif isinstance(data, torch.Tensor):
        return data.cpu()
    else:
        return data


def to_numpy(data):
    """Move data to numpy"""
    if isinstance(data, dict):
        return {k: to_numpy(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [to_numpy(v) for v in data]
    elif isinstance(data, tuple):
        return tuple(to_numpy(v) for v in data)
    elif isinstance(data, set):
        return {to_numpy(v) for v in data}
    elif isinstance(data, torch.Tensor):
        return data.cpu().numpy()
    else:
        return data


def to_cuda(data):
    """Move data to CUDA"""
    if isinstance(data, dict):
        return {k: to_cuda(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [to_cuda(v) for v in data]
    elif isinstance(data, tuple):
        return tuple(to_cuda(v) for v in data)
    elif isinstance(data, set):
        return {to_cuda(v) for v in data}
    elif isinstance(data, torch.Tensor):
        return data.cuda()
    else:
        return data
