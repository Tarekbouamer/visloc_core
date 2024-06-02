import os
from pprint import pprint

from omegaconf import DictConfig, OmegaConf
from rich.console import Console
from rich.syntax import Syntax

try:
    from loguru import logger
except ImportError:
    import logging as logger

    logger.basicConfig(level=logger.INFO)
    logging = logger.getLogger(__name__)


def load_config(cfg_path: str) -> DictConfig:
    """Load config from a YAML/JSON file or a dictionary."""

    if not os.path.exists(cfg_path):
        raise FileNotFoundError(f"Config file not found at {cfg_path}")

    cfg = OmegaConf.load(cfg_path)
    logger.info("Configuration loaded successfully.")
    return cfg


def save_config(cfg: DictConfig, cfg_path: str):
    """Save config to file."""

    OmegaConf.save(cfg, cfg_path)
    logger.info("Configuration saved successfully.")
    return True


def print_config(cfg: DictConfig, format: str = "text"):
    """Print config with optional formats: text, yaml, or json."""
    if format == "yaml":
        print(OmegaConf.to_yaml(cfg))
    else:
        pprint(OmegaConf.to_container(cfg))
    return True


def print_config_color(cfg: DictConfig):
    """Print configuration with color ."""
    console = Console()
    yaml_str = OmegaConf.to_yaml(cfg)
    syntax = Syntax(yaml_str, "yaml", theme="monokai", line_numbers=False)
    console.print(syntax)
    return True
