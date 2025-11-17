import os
from pathlib import Path

from cloudisk.fs.utils import remove_path
from cloudisk.logger import get_logger
from cloudisk.vars import CLOUDISK_ROOT

logger = get_logger("cloudisk.fs")


def init_file_structure(path: Path) -> bool:
    # Handle it asking for user consent
    if path.exists() and not remove_path(path):
        logger.error(f"Failed initializing folder {path}")
        return False

    path.mkdir()
    logger.info(f"Initialialized folder {path} successfully")

    return True


def link_path(src: Path, dst: Path = CLOUDISK_ROOT):
    if not src.exists():
        logger.error(f"'{src}' doesn't exist")

    if src.is_file():
        os.symlink(src, dst / src.name, target_is_directory=True)
        logger.info(f"Linked '{src}' -> '{dst}'")

    if src.is_dir() and (files := os.scandir(src)):
        for file in files:
            os.symlink(file.path, dst / file.name, target_is_directory=True)
            logger.info(f"Linked '{file.path}' -> '{dst}'")


def unlink_path(path: Path):
    if not path.is_symlink():
        logger.error(f"'{path}' is not a symlink")
        return

    os.unlink(path)
    logger.info(f"Unlinked '{path}'")
