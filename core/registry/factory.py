import os
import re
import sys
from collections import defaultdict
from typing import Dict, Optional
import torch
import torch.nn as nn
from loguru import logger
from torch.hub import load_state_dict_from_url
import gdown

# Globally accessible model registries and configurations
_module_to_models = defaultdict(set)
_model_to_module = {}
_model_entrypoints = {}
_model_has_pretrained = set()
_model_pretrained_cfgs = dict()

def load_state_dict(checkpoint_path: str) -> Dict[str, torch.Tensor]:
    """Load model state dict from a given checkpoint path."""
    if os.path.isfile(checkpoint_path):
        state_dict = torch.load(checkpoint_path, map_location="cpu")
        return state_dict
    else:
        logger.error(f"No checkpoint found at {checkpoint_path}")
        raise FileNotFoundError(f"No checkpoint found at {checkpoint_path}")

def load_pretrained(model: nn.Module, variant: str, pretrained_cfg: dict, 
                    state_key: Optional[str] = None, replace: Optional[tuple] = None) -> None:
    """Load pretrained weights into a model from different possible sources."""
    save_folder = "hub"
    os.makedirs(save_folder, exist_ok=True)  # Ensure the directory exists
    save_path = os.path.join(save_folder, f"{variant}.pth")

    try:
        if 'file' in pretrained_cfg and pretrained_cfg['file']:
            state_dict = load_state_dict(pretrained_cfg['file'])
        elif 'url' in pretrained_cfg and pretrained_cfg['url']:
            state_dict = load_state_dict_from_url(pretrained_cfg['url'], map_location="cpu", progress=True)
        elif 'drive' in pretrained_cfg and pretrained_cfg['drive']:
            if not os.path.exists(save_path):
                save_path = gdown.download(pretrained_cfg['drive'], save_path, quiet=False)
            state_dict = load_state_dict(save_path)
        else:
            logger.warning("No pretrained weights specified. Using random initialization.")
            return
    except Exception as e:
        logger.error(f"Error loading pretrained weights: {e}")
        raise

    if state_key:
        state_dict = {k: state_dict[v] for k, v in state_dict.items() if state_key in k}
    if replace:
        state_dict = {k.replace(replace[0], replace[1]): v for k, v in state_dict.items()}

    model.load_state_dict(state_dict, strict=True)

def create_model(model_name: str, cfg: Dict = {}, **kwargs) -> nn.Module:
    """Create a model instance based on its name and optional configuration."""
    if not is_model(model_name):
        raise ValueError(f"Unknown model: {model_name}")
    
    create_fn = model_entrypoint(model_name)
    return create_fn(cfg=cfg, **kwargs)

def is_model(model_name: str) -> bool:
    """Check if a model name is registered."""
    return model_name in _model_entrypoints

def model_entrypoint(model_name: str):
    """Retrieve the factory function for a given model."""
    if model_name in _model_entrypoints:
        return _model_entrypoints[model_name]
    else:
        raise KeyError(f"Model entrypoint not found for {model_name}")

def list_modules() -> list:
    """List all modules that contain registered models."""
    return list(sorted(_module_to_models.keys()))

def is_model_in_modules(model_name: str, module_names: set) -> bool:
    """Check if a model is in one of the specified modules."""
    return any(model_name in _module_to_models[n] for n in module_names)

def is_model_pretrained(model_name: str) -> bool:
    """Check if a model has pretrained weights available."""
    return model_name in _model_has_pretrained

def get_pretrained_cfg(model_name: str) -> dict:
    """Get the pretrained configuration for a model, if available."""
    return _model_pretrained_cfgs.get(model_name, {})

def register_model(fn):
    """Decorator to register a model's factory function."""
    mod = sys.modules[fn.__module__]
    module_name = fn.__module__.split('.')[-1]

    model_name = fn.__name__
    if hasattr(mod, "__all__"):
        mod.__all__.append(model_name)
    else:
        mod.__all__ = [model_name]

    _model_entrypoints[model_name] = fn
    _model_to_module[model_name] = module_name
    _module_to_models[module_name].add(model_name)

    if hasattr(mod, "default_cfgs") and model_name in mod.default_cfgs:
        cfg = mod.default_cfgs[model_name]
        if any(key in cfg for key in ['url', 'file', 'drive']):
            _model_has_pretrained.add(model_name)
            _model_pretrained_cfgs[model_name] = cfg

    return fn

def _natural_key(string_: str):
    """A helper function for natural sort strings."""
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_.lower())]

def list_models(module: str = "", pretrained: bool = False, name_matches_cfg: bool = False) -> list:
    """List available models, optionally filtered by module, pretrained availability, and naming."""
    models = _module_to_models[module] if module else _model_entrypoints.keys()
    if pretrained:
        models = {m for m in models if m in _model_has_pretrained}
    if name_matches_cfg:
        models = {m for m in models if m in _model_pretrained_cfgs}
    return sorted(models, key=_natural_key)
