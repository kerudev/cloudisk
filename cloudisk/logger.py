import logging

LOGGER_CONFIG = {
    "format": "%(asctime)s - %(name)s - [%(levelname)s] - %(message)s",
    "dt_format": "%Y-%m-%d %H:%M:%S",
    "level": logging.INFO,
}


def config_root_logger():
    logging.basicConfig(
        format=LOGGER_CONFIG["format"],
        datefmt=LOGGER_CONFIG["dt_format"],
        level=LOGGER_CONFIG["level"],
    )


def get_logger(name: str = "cloudisk"):
    logger = logging.getLogger(name)
    return logger


config_root_logger()
logger = get_logger()
