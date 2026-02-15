from pathlib import Path

from cloudisk.settings import global_settings

CLOUDISK_ROOT = Path.home() / ".cloudisk"

CLOUDISK_STATIC_DEFAULT = Path(__file__).parent.parent / "templates" / "js"
CLOUDISK_STATIC = Path(global_settings.STATIC_PATH or CLOUDISK_STATIC_DEFAULT).resolve()

CLOUDISK_DB_FILE = ".cloudisk.db"
CLOUDISK_DB_PATH = CLOUDISK_ROOT / CLOUDISK_DB_FILE

MB_1 = 1024 * 1024
MB_100 = MB_1 * 100
