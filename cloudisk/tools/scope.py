from pathlib import Path
from typing import Optional

from sqlalchemy import create_engine

from cloudisk.tools.settings import Settings


class Scope:
    def __init__(  # noqa: D107
        self,
        name: str,
        *,
        engine_path: Optional[Path] = None,
        settings_module: Optional[str] = None,
    ):
        self.name = name
        self.engine_path = engine_path
        self.settings_module = settings_module

        self._engine = None
        self._settings = None

    @property
    def engine(self):
        if self._engine is None:
            self.set_engine()

        return self._engine

    @property
    def settings(self):
        if self._settings is None:
            self._settings = Settings(self.settings_module)

        return self._settings

    def set_engine(self, path: str | Path):
        if path is None:
            path = self.engine_path

        if isinstance(path, Path):
            path = str(path)

        self._engine = self._create_engine(path)

    def cleanup(self):
        self._engine.dispose()
        self._engine = None

    def _create_engine(self, path: str):
        return create_engine(f"sqlite:///{path}")
