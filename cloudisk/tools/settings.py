import os
import shutil
from functools import cache
from pathlib import Path
from typing import Any

from cloudisk.vars import CLOUDISK_ROOT, CLOUDISK_SETTINGS_FILE

from . import _settings


class Settings:
    class Error(Exception):
        """Raised when the problem doesn't fit any of the other exceptions."""

    class BadKeyFormat(Error):  # noqa: N818
        """Raised when the key's format or type is not correct."""

    class Incompatible(Error):  # noqa: N818
        """Raised when the configuration keys are not compatible."""

    def __init__(self, module: str = None, path: Path | str = None):  # noqa: D107
        if module and path:
            raise Settings.Incompatible(
                "Module and path can't be provided at the same time."
            )

        if not module and not path:
            self.module = None
            self.path = CLOUDISK_ROOT / CLOUDISK_SETTINGS_FILE

        if module:
            import importlib

            self.module = importlib.import_module(module) if module else None

        elif path:
            import importlib.util

            spec = importlib.util.spec_from_file_location("settings", path)
            self.module = importlib.util.module_from_spec(spec)

    def __getattr__(self, name: str):  # noqa: D105
        return self.get(name)

    @cache
    def get(self, key: str, default: Any = None) -> str:
        """
        Return the value of `key` in the defined settings.

        The `key` is searched first in `self.module`. If it is not found, it's
        searched as an environment variable.

        Parameters
        ----------
        key: str
            The key to get.
        default: Any = None
            The default value in case `key` doesn't exist.

        Returns
        -------
        str
            The value.
        """
        self._check_key(key)

        value = None

        if self.module:
            value = getattr(self.module, key, default)

        return value or os.environ.get(f"CLOUDISK_{key}") or default

    def set_default(self, **kwargs):
        """
        Set default values for each key in `kwargs`.
        If `key` exists, the default value is not applied.
        """
        for key, value in kwargs.items():
            self._check_key(key)

            if not self.module:
                os.environ.setdefault(f"CLOUDISK_{key}", str(value))
                continue

            if key not in self.module.__dict__:
                self.module.__dict__.setdefault(key, value)
                continue

            if isinstance(self.module.__dict__[key], type(Ellipsis)):
                self.module.__dict__[key] = value

    def clear_cache(self):
        """Clear cache for all functions and properties inside the instance."""
        self.get.cache_clear()

    @staticmethod
    def build_module(path: Path):
        """
        Build a settings module from parameters.

        Parameters
        ----------
        path: Path
            The path of the settings module.
        """
        shutil.copyfile(_settings.default.__file__, path)

    def _check_key(self, key: str):
        """
        Check if the key has a correct format.

        Parameters
        ----------
        key: str
            The key to check.

        Raises
        ------
        BadKeyFormat
            - The key is not a string.
            - Not all characters are uppercase.
        """
        if not isinstance(key, str):
            raise Settings.BadKeyFormat("key must be a string")

        if key.upper() != key:
            raise Settings.BadKeyFormat("All characters in key must be uppercase")
