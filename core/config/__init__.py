from loguru import logger
from omegaconf import OmegaConf


def load_cfg(cfg_path, default_cfg_path=None):
    """Load config from file"""
    # load config
    cfg = OmegaConf.load(cfg_path)

    # merge default config
    if default_cfg_path:
        default_cfg = OmegaConf.load(default_cfg_path)
        cfg = OmegaConf.merge(default_cfg, cfg)

    # log config
    logger.info(OmegaConf.to_yaml(cfg))

    return cfg
