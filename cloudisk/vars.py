from pathlib import Path

CLOUDISK_ROOT = Path.home() / ".cloudisk"

CLOUDISK_DB_FILE = ".cloudisk.db"
CLOUDISK_DB_PATH = CLOUDISK_ROOT / CLOUDISK_DB_FILE

CLOUDISK_SETTINGS_FILE = "settings.py"

MB_1 = 1024 * 1024
MB_100 = MB_1 * 100
