import os
from pathlib import Path

from cloudisk.fs.utils import remove_path
from cloudisk.logger import get_logger
from cloudisk.vars import CLOUDISK_ROOT

logger = get_logger("cloudisk.fs")


def init_cloudisk_folder() -> bool:
    # Handle it asking for user consent
    if CLOUDISK_ROOT.exists() and not remove_path(CLOUDISK_ROOT):
        logger.error(f"Failed initializing folder {CLOUDISK_ROOT}")
        return False

    CLOUDISK_ROOT.mkdir()
    logger.info(f"Initialized folder {CLOUDISK_ROOT} successfully")

    return True


# TODO handle dst exists
def link_path(path: Path, dst: Path = CLOUDISK_ROOT):
    if not path.exists():
        logger.error(f"'{path}' doesn't exist")

    if path.is_file():
        os.symlink(path, dst / path.name, target_is_directory=True)
        logger.info(f"Linked '{path}' -> '{dst}'")

    if path.is_dir() and (files := os.scandir(path)):
        for file in files:
            os.symlink(file.path, dst / file.name, target_is_directory=True)
            logger.info(f"Linked '{file.path}' -> '{dst}'")


def unlink_path(path: Path):
    if not path.is_symlink():
        logger.error(f"'{path}' is not a symlink")
        return

    os.unlink(path)
    logger.info(f"Unlinked '{path}'")
