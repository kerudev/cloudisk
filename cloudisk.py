import os
import shutil
import logging
from pathlib import Path

# Directory name to store files
STORAGE_NAME = ".cloudisk"
LOGGER = logging.getLogger("cloudisk.entry_point")


def ask_remove(storage_path: Path) -> bool:
    while (
        remove := input(
            f"{storage_path} already exists. Do you want to remove it? (y/n)\n"
        )
    ) not in ("y", "n"):
        LOGGER.error(f"Unexpected answer. Expected 'y' or 'n', got {remove}")

    return remove != "n"


def remove_file(storage_path: Path):
    storage_path.unlink()


def remove_dir(storage_path: Path) -> bool:
    # If dir is empty
    if not os.listdir(storage_path):
        storage_path.rmdir()

    else:
        if ask_empty_dir(storage_path) is False:
            return False

        shutil.rmtree(storage_path)

    return True


def ask_empty_dir(storage_path: Path) -> bool:
    while (
        empty_dir := input(
            f"Dir {storage_path} is not empty. Do you want to remove all of its content? (y/n)\n"
        )
    ) not in ("y", "n"):
        LOGGER.error(f"Unexpected answer. Expected 'y' or 'n', got {empty_dir}")

    return empty_dir != "n"


def handle_storage_path_exists(storage_path: Path) -> bool:
    if ask_remove(storage_path) is False:
        return False

    if storage_path.is_file():
        remove_file(storage_path)

    elif storage_path.is_dir():
        if remove_dir(storage_path) is False:
            return False

    else:
        raise Exception(
            f"{storage_path} already exists and is not a file or a directory. "
            "Please, remove it first."
        )

    return True


def main():
    home_dir = Path.home()
    storage_path = home_dir / STORAGE_NAME

    if storage_path.exists():
        # Handle it asking for user consent
        if handle_storage_path_exists(storage_path) is False:
            return False

    storage_path.mkdir()


if __name__ == "__main__":
    main()
