import os
from pathlib import Path

CLOUDISK_ROOT = (Path.home() / ".cloudisk").resolve()

CLOUDISK_STATIC_DEFAULT = Path(__file__).parent.parent / "static"
CLOUDISK_STATIC_ENV = os.environ.get("CLOUDISK_STATIC")
CLOUDISK_STATIC = Path(CLOUDISK_STATIC_ENV or CLOUDISK_STATIC_DEFAULT).resolve()

METADATA_FILE = ".metadata.db"
METADATA_PATH = (CLOUDISK_ROOT / METADATA_FILE).resolve()

MB_1 = 1024 * 1024
MB_100 = MB_1 * 100
