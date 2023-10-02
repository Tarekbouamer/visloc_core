import torch


def to_numpy(data):
    """Inplace move data to numpy """
    if isinstance(data, dict):
        for k, v in data.items():
            data[k] = to_numpy(v)
        return data
    elif isinstance(data, list):
        for i, v in enumerate(data):
            data[i] = to_numpy(v)
        return data
    elif isinstance(data, tuple):
        return tuple(to_numpy(v) for v in data)
    elif isinstance(data, set):
        return {to_numpy(v) for v in data}
    elif isinstance(data, torch.Tensor):
        return data.cpu().numpy()
    else:
        return data


def to_cpu(data):
    """Inplace move data to CPU """
    if isinstance(data, dict):
        for k, v in data.items():
            data[k] = to_cpu(v)
        return data
    elif isinstance(data, list):
        for i, v in enumerate(data):
            data[i] = to_cpu(v)
        return data
    elif isinstance(data, tuple):
        return tuple(to_cpu(v) for v in data)
    elif isinstance(data, set):
        return {to_cpu(v) for v in data}
    elif isinstance(data, torch.Tensor):
        return data.cpu()
    else:
        return data


def to_cuda(data):
    """Inplace move data to CUDA """
    if isinstance(data, dict):
        for k, v in data.items():
            data[k] = to_cuda(v)
        return data
    elif isinstance(data, list):
        for i, v in enumerate(data):
            data[i] = to_cuda(v)
        return data
    elif isinstance(data, tuple):
        return tuple(to_cuda(v) for v in data)
    elif isinstance(data, set):
        return {to_cuda(v) for v in data}
    elif isinstance(data, torch.Tensor):
        return data.cuda()
    else:
        return data
