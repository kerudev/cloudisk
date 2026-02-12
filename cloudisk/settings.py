import os


class Settings:
    def __init__(self, module: str):  # noqa: D107
        self.module = module

    def get(self, key: str, default: str) -> str:
        """
        Return the value of `key` in the defined settings.

        The `key` is searched as an environment variable. If it does't exist,
        it's searched in `self.module`.

        Parameters
        ----------
        key: str
            The key to get.
        default: str
            The default value in case `key` doesn't exist.

        Returns
        -------
        str
            The value.
        """
        if isinstance(key, str):
            raise Exception("key must be a string")

        if key.upper() != key:
            raise Exception("key must have all uppercase")

        if env := os.environ.get(f"CLOUDISK_{key}"):
            return env

        settings = __import__(self.module)
        var = getattr(settings, key, default)

        return var
