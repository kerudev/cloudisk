import json
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from pydantic import BaseModel
from pydantic.fields import Field

from cloudisk.fs.commands import init_file_structure
from cloudisk.vars import CLOUDISK_ROOT, METADATA_FILE

ENCODING = "utf-8"
ENSURE_ASCII = False


class Metadata(BaseModel):
    file_uuid: str = Field(default_factory=lambda: str(uuid4()))

    version: str = "1.0"
    content_type: str = Field(...)
    status: int = Field(default=1)

    created_at: int = Field(default_factory=lambda: int(datetime.now().timestamp()))
    updated_at: int = int(datetime.now().timestamp())
    deleted_at: int = Field(default=0)

    file_name: str = Field(...)
    file_type: str = Field(...)
    file_path: str = Field(...)
    file_size: int = Field(...)

    extra_data: dict[str, Any] = Field(default_factory=dict)


# region Private methods
def _init_metadata_file() -> bool:
    if not Path(CLOUDISK_ROOT).is_dir():
        init_file_structure(CLOUDISK_ROOT)
    return METADATA_FILE.is_file()


def _save(data: dict):
    with open(METADATA_FILE, "w", encoding=ENCODING) as f:
        json.dump(data, f, ensure_ascii=ENSURE_ASCII, indent=4)


def _load() -> dict:
    if not METADATA_FILE.is_file():
        return {"error": "Metadata file does not exist."}

    with open(METADATA_FILE, "r", encoding=ENCODING) as f:
        return json.load(f)


# endregion


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
        with open(METADATA_FILE, "w", encoding=ENCODING) as f:
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
    return data[name] if file_exists(data[name]) == 0 else {}


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
    deleted_at = data.get("deleted_at", 0)
    status = data.get("status", 0)
    return deleted_at == 0 and status == 1


def update_metadata(name: str, **extra) -> dict:
    """
    Update `extra` fields for the file selected.

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
    data[name]["extra_data"].update(extra["extra_data"])
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
            name="test",
            metadata=Metadata(
                content_type="text/plain",
                file_type="txt",
                file_name="test.txt",
                file_path="/some/path/test.txt",
                file_size=1234,
                extra_data={"author": "gandordev"},
            ),
        )
    )
    input("----------------------------------------------------------")
    print(read_metadata(name="test"))
    input("----------------------------------------------------------")
    print(update_metadata(name="test", extra={"something": "foo"}))
    input("----------------------------------------------------------")
    print(list_file_names())
    input("----------------------------------------------------------")
    print(delete_metadata(name="test"))
"""
