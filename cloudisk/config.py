from pathlib import Path
from tomllib import load

PYPROJECT_TOML_PATH = Path(__file__).parent / "pyproject.toml"


def load_config():
    if not PYPROJECT_TOML_PATH.is_file():
        return {}

    with open(PYPROJECT_TOML_PATH, "rb") as f:
        config = load(f)

    return config


config = load_config()
