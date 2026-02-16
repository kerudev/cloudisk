from pathlib import Path

from cloudisk.globals import settings

CLOUDISK_STATIC = Path(settings.STATIC_PATH).resolve()
