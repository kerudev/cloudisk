import os
from pathlib import Path

CLOUDISK_ROOT = Path.home() / ".cloudisk"

CLOUDISK_STATIC_DEFAULT = Path(__file__).parent.parent / "templates" / "js"
CLOUDISK_STATIC_ENV = os.environ.get("CLOUDISK_STATIC")
CLOUDISK_STATIC = Path(CLOUDISK_STATIC_ENV or CLOUDISK_STATIC_DEFAULT).resolve()

CLOUDISK_DB_FILE = ".cloudisk.db"
CLOUDISK_DB_PATH = CLOUDISK_ROOT / CLOUDISK_DB_FILE

MB_1 = 1024 * 1024
MB_100 = MB_1 * 100
