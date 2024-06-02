from typing import List, Optional, Tuple, Union

import numpy as np
import torch
import torchvision.transforms as tfn

# Constants for ImageNet normalization
IMAGENET_DEFAULT_MEAN = [0.485, 0.456, 0.406]
IMAGENET_DEFAULT_STD = [0.229, 0.224, 0.225]

tfn_image_net = tfn.Normalize(mean=IMAGENET_DEFAULT_MEAN, std=IMAGENET_DEFAULT_STD)
tfn_grayscale = tfn.Grayscale()


class ToTensor:
    """Convert a NumPy image array to a PyTorch tensor with optional dtype specification."""
    def __init__(self, dtype=torch.float32):
        self.dtype = dtype

    def __call__(self, np_img):
        # Ensure image has three dimensions if it is not
        if np_img.ndim < 3:
            np_img = np.expand_dims(np_img, axis=-1)
        # Change dimension order to CxHxW for PyTorch compatibility
        np_img = np_img.transpose((2, 0, 1))
        # Convert numpy array to PyTorch tensor and set data type
        tensor_img = torch.from_numpy(np_img).to(dtype=self.dtype)
        return tensor_img


def make_transforms(normalize="imagenet", gray=False):
    """
    Create a torchvision transform sequence for basic image processing.
    Args:
    - normalize (str): Specifies the normalization method ('imagenet' or None).
    - gray (bool): Indicates whether to convert images to grayscale.
    """
    tfl = []

    # 
    if gray:
        tfl.append(tfn_grayscale)

    # image normalization
    if normalize == "imagenet":
        tfl.append(tfn_image_net)

    return tfn.Compose(tfl)


def create_train_transform(
    input_size: Optional[int] = None,
    scale: Optional[Tuple[float, float]] = None,
    ratio: Optional[Tuple[float, float]] = None,
    hflip_prob: Optional[float] = 0.5,
    vflip_prob: Optional[float] = 0.0,
    color_jitter: Union[float, Tuple[float, ...]] = 0.4,
    color_jitter_prob: Optional[float] = None,
    grayscale_prob: float = 0.,
    gaussian_blur_prob: float = 0.,
    interpolation: str = "bilinear",
    mean: Optional[List[float]] = IMAGENET_DEFAULT_MEAN,
    std: Optional[List[float]] = IMAGENET_DEFAULT_STD,
) -> tfn.Compose:
    """
    Create a comprehensive transform pipeline for training data augmentation.
    """
    transforms = []

    # random resized crop   
    if input_size and scale and ratio:
        transforms.append(tfn.RandomResizedCrop(input_size, scale=scale, ratio=ratio, interpolation=interpolation))

    # horizontal flip
    if hflip_prob:
        transforms.append(tfn.RandomHorizontalFlip(p=hflip_prob))

    # vertical flip
    if vflip_prob:
        transforms.append(tfn.RandomVerticalFlip(p=vflip_prob))

    # color jitter
    if color_jitter_prob is not None:
        transforms.append(tfn.RandomApply([tfn.ColorJitter(color_jitter)], p=color_jitter_prob))

    # grayscale
    if grayscale_prob > 0:
        transforms.append(tfn.RandomGrayscale(p=grayscale_prob))

    # gaussian blur
    if gaussian_blur_prob > 0:
        transforms.append(tfn.GaussianBlur(kernel_size=int(0.1 * input_size), sigma=(0.1, 2.0)))

    # to tensor
    transforms.append(tfn.ToTensor())
    
    # normalize
    transforms.append(tfn.Normalize(mean=mean, std=std))

    return tfn.Compose(transforms)


def create_eval_transform(
    resize: Optional[int] = None,
    mean: Optional[List[float]] = IMAGENET_DEFAULT_MEAN,
    std: Optional[List[float]] = IMAGENET_DEFAULT_STD,
) -> tfn.Compose:
    """
    Create a transform pipeline for evaluation, focused on resizing and normalization.
    """
    transforms = []

    # resize
    if resize:
        transforms.append(tfn.Resize(resize))

    # to tensor
    transforms.append(tfn.ToTensor())
    
    # normalize  
    transforms.append(tfn.Normalize(mean=mean, std=std))

    return tfn.Compose(transforms)
