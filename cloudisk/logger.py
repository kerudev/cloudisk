import logging
from typing import Literal, TypedDict


class LoggerConfig(TypedDict):
    format: str
    datefmt: str
    level: Literal[10, 20, 30, 40, 50]


DEFAULT_CONFIG: LoggerConfig = {
    "format": "%(asctime)s - %(name)s - [%(levelname)s] - %(message)s",
    "datefmt": "%Y-%m-%d %H:%M:%S",
    "level": 20,
}


def config_root_logger(config: LoggerConfig = DEFAULT_CONFIG) -> None:
    """
    Apply config to the root logger.

    Parameters
    ----------
    config : dict
        Basic configuration to apply to the root logger.
    """
    logging.basicConfig(
        format=config["format"], datefmt=config["datefmt"], level=config["level"]
    )


def get_logger(name: str = "cloudisk") -> logging.Logger:
    """
    Get logger with name parameter.

    Parameters
    ----------
    name : str
        Logger name to be returned.

    Returns
    -------
    logging.Logger
        Created logger with name parameter.
    """
    logger = logging.getLogger(name)
    return logger


config_root_logger()
logger = get_logger()
