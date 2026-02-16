import os
from functools import cache


class Settings:
    class Error(Exception):
        """Raised when the problem doesn't fit any of the other exceptions."""

    class BadKeyFormat(Error):  # noqa: N818
        """Raised when the key's format or type is not correct."""

    def __init__(self, module: str = None):  # noqa: D107
        self.module = __import__(module) if module else None

    def __getattr__(self, name: str):  # noqa: D105
        return self.get(name)

    @cache
    def get(self, key: str, default: str = None) -> str:
        """
        Return the value of `key` in the defined settings.

        The `key` is searched first in `self.module`. If it is not found, it's
        searched as an environment variable.

        Parameters
        ----------
        key: str
            The key to get.
        default: str = None
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

    def set_default(self, **kwargs):  # noqa: D105
        for key, value in kwargs.items():
            self._check_key(key)

            if self.module:
                self.module.__dict__.setdefault(key, value)
            else:
                os.environ.setdefault(f"CLOUDISK_{key}", value)

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
