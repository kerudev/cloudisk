import os
from pathlib import Path

import typer

from cloudisk.fs.utils import ask_remove_dir, ask_remove_path
from cloudisk.logger import get_logger
from cloudisk.tools.settings import Settings
from cloudisk.vars import CLOUDISK_DB_FILE, CLOUDISK_ROOT, CLOUDISK_SETTINGS_FILE

logger = get_logger("cloudisk.fs")


def init_cloudisk_root() -> bool:
    """
    Initialize cloudisk folder and handle if it already exists.

    Returns
    -------
    bool
        True if created. False otherwise.
    """
    # Handle it asking for user consent
    if CLOUDISK_ROOT.exists() and not ask_remove_path(CLOUDISK_ROOT):
        logger.error(f"Failed initializing folder '{CLOUDISK_ROOT}'")
        return False

    CLOUDISK_ROOT.mkdir()
    logger.info(f"Initialized folder '{CLOUDISK_ROOT}' successfully")

    return True


def _try_link(src: Path, dst: Path) -> None:
    """
    Try to make a symlink from src path to dst path.

    Parameters
    ----------
    src : Path
        Source path to make symlink from.
    dst : Path
        Destination path to make symlink to.
    """
    try:
        os.symlink(src, dst)
        logger.info(f"Linked '{src}' -> '{dst}'")
    except FileExistsError:
        logger.info(f"Already linked: '{src}'")

    # Raised on Windows when the user doesn't have Developer Mode on
    # https://docs.python.org/3/library/os.html#os.symlink
    except OSError as e:  # pragma: no cover
        if not os.name == "nt":
            raise e

        raise OSError(
            "The symlink could not be created. "
            "Make sure Developer Mode is on and try again."
        ) from e


def link_path(path: Path, recursive: bool = False) -> None:
    """
    Create a symlink to `path`.

    Parameters
    ----------
    path : Path
        The path to link.
    recursive : bool = False
        Whether the link is recursive or not.
        If `True` and `path` is a directory, it's contents will be linked.
    """
    if not path.exists():
        logger.error(f"'{path}' doesn't exist")
        return

    dst = CLOUDISK_ROOT / path.name

    if dst.exists():
        logger.error(f"'{dst}' already exists")
        return

    if not recursive or path.is_file():
        _try_link(path, dst)
        return

    for file in os.scandir(path):
        _try_link(path / file.name, CLOUDISK_ROOT / file.name)


def unlink_path(path: Path) -> None:
    """
    Remove linked path.

    Parameters
    ----------
    path : Path
        Path to be unlinked.
    """
    if not path.is_symlink():
        logger.error(f"'{path}' is not a symlink")
        return

    os.unlink(path)
    logger.info(f"Unlinked '{path}'")


def create_space(name: str, protect: bool = False) -> None:
    from cloudisk.db.models import Space

    if not CLOUDISK_ROOT.exists():
        init_cloudisk_root()

    space_path = CLOUDISK_ROOT / name

    if space_path.exists():
        if not ask_remove_dir(space_path):
            return

        Space().remove(name=name)

    space_path.mkdir(exist_ok=True)

    Settings.build_module(CLOUDISK_ROOT / CLOUDISK_SETTINGS_FILE)
    Space().create(name=name, protect=protect)

    logger.info(f"Created the '{name}' space")


def use_space(name: str) -> None:
    from cloudisk.db.models import Space

    if not CLOUDISK_ROOT.exists():
        init_cloudisk_root()  # pragma: no cover

    space_path = CLOUDISK_ROOT / name

    if not space_path.exists():
        logger.error(f"Space '{name}' doesn't exist.")
        return

    Space().use(name=name)

    logger.info(f"Using space '{name}'")


# TODO maybe a space is in the database but not found in ROOT
def list_spaces() -> None:
    spaces = Space().list()

    if spaces:
        typer.echo("Tracked spaces:")
        for space in spaces:
            typer.echo(f"- {space}")

    root = os.listdir(CLOUDISK_ROOT)
    root = [x for x in root if x != CLOUDISK_DB_FILE]

    if len(root):
        untracked = list(filter(lambda x: x not in spaces, root))

        message = "Untracked spaces:"
        if spaces:
            message = "\n" + message

        typer.echo(message)
        for space in untracked:
            typer.echo(f"- {space}")

        return
