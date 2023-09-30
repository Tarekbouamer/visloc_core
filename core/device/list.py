import torch


def flatten_list_of_tensors(data: dict):
    """Flatten list of tensors"""
    for k, v in data.items():
        if isinstance(v, list):
            data[k] = torch.cat(v, dim=0)
    return data
