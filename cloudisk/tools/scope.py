from pathlib import Path
from typing import Any, Optional

from sqlalchemy import inspect, text
from sqlmodel import Session

from cloudisk.tools.settings import Settings
from cloudisk.vars import CLOUDISK_ROOT, CLOUDISK_SETTINGS_FILE


class Scope:
    def __init__(  # noqa: D107
        self,
        name: str,
        *,
        engine_path: Optional[Path] = None,
        settings_path: Optional[str] = None,
        settings_module: Optional[str] = None,
        extras: Optional[dict[str, Any]] = None,
    ):
        self.name = name
        self.engine_path = engine_path
        self.settings_path = settings_path
        self.settings_module = settings_module

        self.extras = extras or {}

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
            self._settings = Settings(
                module=self.settings_module,
                path=self.settings_path,
            )

        return self._settings

    def set_engine(self, path: Optional[str | Path] = None):
        if path is None:
            path = self.engine_path

        self._engine = self._create_engine(path)

    def update_space(self):
        if not self.engine:
            return

        if not inspect(self.engine).has_table("space"):
            return

        with Session(self.engine) as session:
            # Query without using the Space model manager to avoid circular imports
            result = session.exec(text("SELECT id, name FROM space WHERE space.used = 1"))
            space = result.one_or_none()

            if not space:
                count = session.exec(text("COUNT(*) FROM space"))
                space = count

                return

            space_id, space_name = space

            space_path = CLOUDISK_ROOT / space_name
            self.settings_path = space_path / CLOUDISK_SETTINGS_FILE

            # TODO refresh this value on runtime
            self.extras["space_id"] = space_id
            self.extras["space_name"] = space_name

    def cleanup(self):
        self._engine.dispose()
        self._engine = None

    def _create_engine(self, path: Path):
        from sqlalchemy import create_engine

        if not path.parent.exists():
            path.parent.mkdir()

        return create_engine(f"sqlite:///{str(path)}")
