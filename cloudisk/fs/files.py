import json
from datetime import datetime
from typing import Any

from cloudisk import fs
from cloudisk.fs.vars import METADATA_FILE

_ENCODING = "utf-8"
_ENSURE_ASCII = False


# region Private methods
def _init_metadata_file() -> bool:
    if METADATA_FILE.exists():
        return True  # Ya existe, todo fino
    return fs.init_file_structure(METADATA_FILE)


def _save(data: dict):
    with open(METADATA_FILE, "w", encoding=_ENCODING) as f:
        json.dump(data, f, ensure_ascii=_ENSURE_ASCII, indent=4)


def _load() -> dict:
    if not METADATA_FILE.is_file():
        return {"error": "Metadata file does not exist."}

    with open(METADATA_FILE, "r", encoding=_ENCODING) as f:
        return json.load(f)


# endregion


def create_metadata(
    name: str, content_type: str, path: str, size: int, **extra: Any
) -> dict:
    """
    Create a metadata as a json file for the recent file created.

    Parameters
    ----------
    name : str
        Name of the file
    content_type : str
        Extension of the file
    path : str
        Where the file is stored
    size : int
        How much the file weights
    extra: Any
        Any extra medatada considered important

    Returns
    -------
    dict
        Either an error or metadata created

    Raises
    ------
    ValueError
        File already exist
    """
    # If folder does not exist, we initialize it
    if not _init_metadata_file():
        with open(METADATA_FILE, "w", encoding=_ENCODING) as f:
            json.dump({}, f, ensure_ascii=_ENSURE_ASCII)

    data = _load()
    if "error" in data:
        return data

    if name in data:
        raise ValueError(f"File with name {name} already exist")

    # Adjusts params
    cur_time = int(datetime.now().timestamp())
    metadata = {
        "name": name,
        "content-type": content_type,
        "path": path,
        "size": size,
        "created_at": cur_time,
        "updated_at": cur_time,
        **extra,  # Any extra metadata the user wants to include
    }

    # Save file
    data.update({name: metadata})
    _save(data)
    return metadata


def read_metadata(name: str) -> dict:
    """
    Get metadata of the file selected.

    Parameters
    ----------
    name : str
        Name of the file

    Returns
    -------
    dict
        Metadata

    Raises
    ------
    KeyError
        The metadata file does not exist
    """
    data = _load()

    if name not in data:
        raise KeyError(f"No metadata file exists for '{name}'")
    return data[name]


def update_metadata(name: str, **extra) -> dict:
    """
    Update `updates` fields for the file selected.

    Parameters
    ----------
    name : str
        Name of the file
    extra: Any
        Any extra medatada considered important

    Returns
    -------
    dict
        Updated metadata

    Raises
    ------
    KeyError
        The metadata file does not exist
    """
    data = _load()
    if name not in data:
        raise KeyError(f"No metadata file exists for '{name}'")

    # Updated keys
    data[name].update(extra)
    data[name]["updated_at"] = int(datetime.now().timestamp())

    # Save data
    _save(data)
    return data[name]


def delete_metadata(name: str):
    """
    Delete metadata of the selected file.

    Parameters
    ----------
    name : str
        Name of the file

    Raises
    ------
    KeyError
        The metadata file does not exist
    """
    data = _load()
    if name not in data:
        raise KeyError(f"No metadata file exists for '{name}'")

    # Delete metadata of the selected file
    del data[name]
    _save(data)


def list_file_names() -> list:
    """
    Get the names of all the files saves in the clouddisk dir.

    Returns
    -------
    list
        Names of the files
    """
    data = _load()

    names = list(data)
    return list(names)


"""
if __name__ == "__main__":
    print(
        create_metadata(
            name="test", content_type="json", path=str(METADATA_FILE_PATH), size=1
        )
    )
    print(read_metadata(name="test"))
    print(update_metadata(name="test", extra={"something":"foo"}))
    print(list_file_names())
    print(delete_metadata(name="test"))
"""
