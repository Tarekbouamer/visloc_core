import numpy as np


def pad_image_bottom_right(img, pad_size, ret_mask=False):
    """ Pad image to padding_size with zeros"""

    assert isinstance(pad_size, int) and pad_size >= max(img.shape[-2:]), \
        f"{pad_size} < {max(img.shape[-2:])}"

    # mask
    mask = None

    if img.ndim == 2:
        padded = np.zeros((pad_size, pad_size), dtype=img.dtype)
        padded[:img.shape[0], :img.shape[1]] = img
        if ret_mask:
            mask = np.zeros((pad_size, pad_size), dtype=bool)
            mask[:img.shape[0], :img.shape[1]] = True
    elif img.ndim == 3:
        padded = np.zeros((img.shape[0], pad_size, pad_size), dtype=img.dtype)
        padded[:, :img.shape[1], :img.shape[2]] = img

        if ret_mask:
            mask = np.zeros((img.shape[0], pad_size, pad_size), dtype=bool)
            mask[:, :img.shape[1], :img.shape[2]] = True
    else:
        raise ValueError("img.ndim must be 2 or 3")

    return padded, mask
