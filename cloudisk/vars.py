from pathlib import Path

CLOUDISK_ROOT = (Path.home() / ".cloudisk").resolve()
CLOUDISK_STATIC = (Path(__file__).parent / "static").resolve()

METADATA_FILE = ".metadata.db"
METADATA_PATH = (CLOUDISK_ROOT / METADATA_FILE).resolve()

MB_1 = 1024 * 1024
MB_100 = 100 * MB_1
