"""Contains global variables that refer to the global state in runtime."""

from pathlib import Path

from cloudisk.context import Context
from cloudisk.settings import Settings

context = Context()

settings = Settings()
settings.set_default(STATIC_PATH=str(Path(__file__).parent.parent / "templates" / "js"))
