import os
from functools import cache


class Settings:
    def __init__(self, module: str = None):  # noqa: D107
        self.module = module

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
        if not isinstance(key, str):
            raise Exception("key must be a string")

        if key.upper() != key:
            raise Exception("All characters in key must be uppercase")

        value = None

        if self.module:
            settings = __import__(self.module)
            value = getattr(settings, key, default)

        return value or os.environ.get(f"CLOUDISK_{key}") or default


global_settings = Settings()
