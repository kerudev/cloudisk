import json
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from cloudisk.fs.commands import init_file_structure
from cloudisk.vars import CLOUDISK_ROOT, METADATA_PATH

ENCODING = "utf-8"
ENSURE_ASCII = False


class Metadata(BaseModel):
    file_uuid: UUID

    version: str = "1.0"
    content_type: str
    available: bool = True

    created_at: int = 0
    updated_at: int = 0
    deleted_at: int = 0

    file_name: str
    file_type: str
    file_path: str
    file_size: int

    extra: dict[str, Any] = Field(default_factory=dict)

    def model_post_init(self, context: Any) -> None:  # noqa
        now = int(datetime.now().timestamp())

        self.file_uuid = str(uuid4())

        self.created_at = now
        self.updated_at = now


# region Private methods
def _init_metadata_file() -> bool:
    if not Path(CLOUDISK_ROOT).is_dir():
        init_file_structure(CLOUDISK_ROOT)
    return METADATA_PATH.is_file()


def _save(data: dict):
    with open(METADATA_PATH, "w", encoding=ENCODING) as f:
        json.dump(data, f, ensure_ascii=ENSURE_ASCII, indent=4)


def _load() -> dict:
    if not METADATA_PATH.is_file():
        return {"error": "Metadata file does not exist."}

    with open(METADATA_PATH, "r", encoding=ENCODING) as f:
        return json.load(f)


# endregion


# TODO refector functions to be inside the Metadata model


def create_metadata(name: str, metadata: Metadata) -> dict:
    """
    Create a metadata as a json file for the recent file created.

    Parameters
    ----------
    name : str
        Name of the file
    metadata : Metadata
        Metadata object

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
        with open(METADATA_PATH, "w", encoding=ENCODING) as f:
            json.dump({}, f, ensure_ascii=ENSURE_ASCII)

    data = _load()
    if "error" in data:
        return data

    if name in data:
        raise ValueError(f"File with name {name} already exist")

    # Adjusts params
    # Ensure the Pydantic model has the correct file name and a fresh updated_at timestamp
    metadata_dict = metadata.model_copy(update={"file_name": name}).model_dump()

    # Save file
    data.update({name: metadata_dict})
    _save(data)
    return metadata_dict


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

    # File is active
    return data[name] if file_exists(data[name]) else {}


def file_exists(data: dict) -> bool:
    """
    Check from metadata if file exists.

    Parameters
    ----------
    data : dict
        Metadata of the file

    Returns
    -------
    bool
        True if file exists, False otherwise
    """
    return data.get("available", False)


def update_metadata(name: str, **kwargs: Any) -> dict:
    """
    Update `extra` fields for the file selected.

    Parameters
    ----------
    name : str
        Name of the file
    kwargs : Any
        Any extra metadata considered important

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
    data[name].setdefault("extra", {}).update(kwargs)
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
    """
    data = _load()
    data.pop(name, None)

    _save(data)


def list_file_names() -> list[str]:
    """
    Get the names of all the files saves in the cloudisk dir.

    Returns
    -------
    list[str]
        Names of the files
    """
    data = _load()

    return list(data)
