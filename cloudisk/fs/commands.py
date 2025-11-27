import os
from pathlib import Path

from cloudisk.fs.utils import ask_remove_path
from cloudisk.logger import get_logger
from cloudisk.vars import CLOUDISK_ROOT

logger = get_logger("cloudisk.fs")


def init_cloudisk_folder() -> bool:
    # Handle it asking for user consent
    if CLOUDISK_ROOT.exists() and not ask_remove_path(CLOUDISK_ROOT):
        logger.error(f"Failed initializing folder {CLOUDISK_ROOT}")
        return False

    CLOUDISK_ROOT.mkdir()
    logger.info(f"Initialized folder {CLOUDISK_ROOT} successfully")

    return True


def link_path(path: Path):
    """
    Create a symlink to `path`.

    Parameters
    ----------
    path : Path
        The path to link.
    """
    if not path.exists():
        logger.error(f"'{path}' doesn't exist")
        return

    dst = CLOUDISK_ROOT / path.name

    if dst.exists():
        logger.error(f"'{dst}' already exists")
        return

    os.symlink(path, dst, target_is_directory=True)
    logger.info(f"Linked '{path}' -> '{dst}'")


def unlink_path(path: Path):
    if not path.is_symlink():
        logger.error(f"'{path}' is not a symlink")
        return

    os.unlink(path)
    logger.info(f"Unlinked '{path}'")
