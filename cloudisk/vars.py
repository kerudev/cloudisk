from pathlib import Path

CLOUDISK_ROOT = Path.home() / ".cloudisk"
METADATA_FILE = CLOUDISK_ROOT / ".metadata.json"
CLOUDISK_STATIC = Path(__file__).parent / "static"
