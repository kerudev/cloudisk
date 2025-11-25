from pathlib import Path

CLOUDISK_ROOT = (Path.home() / ".cloudisk").resolve()
CLOUDISK_STATIC = (Path(__file__).parent / "static").resolve()

METADATA_FILE = ".metadata.json"
METADATA_PATH = (CLOUDISK_ROOT / METADATA_FILE).resolve()
