"""Contains global variables that refer to the global state in runtime."""

from pathlib import Path

from cloudisk.tools import Context, Scope
from cloudisk.vars import CLOUDISK_DB_PATH

root = Scope("root", engine_path=CLOUDISK_DB_PATH)

root.update_space()
root.settings.set_default(
    STATIC_PATH=str(Path(__file__).parent.parent / "templates" / "js")
)

context = Context(scopes=[root])

# TMP
settings = root.settings
