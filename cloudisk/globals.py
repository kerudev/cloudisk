"""Contains global variables that refer to the global state in runtime."""

import os
from pathlib import Path

from cloudisk.tools import Context, Scope
from cloudisk.vars import CLOUDISK_DB_PATH

os.environ.setdefault(
    "CLOUDISK_STATIC_PATH",
    str(Path(__file__).parent.parent / "templates" / "js"),
)

context = Context(scopes=[Scope("root", engine_path=CLOUDISK_DB_PATH)])

# TMP
settings = context.root.settings
