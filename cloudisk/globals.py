"""Contains global variables that refer to the global state in runtime."""

from pathlib import Path

from cloudisk.tools import Context, Scope
from cloudisk.vars import CLOUDISK_DB_PATH

root_scope = Scope(
    "root",
    engine_path=CLOUDISK_DB_PATH,
    settings_module="cloudisk.tools._settings.default",
)

root_scope.settings.set_default(
    STATIC_PATH=str(Path(__file__).parent.parent / "templates" / "js")
)

# TMP
settings = root_scope.settings

context = Context(scopes=[root_scope])
