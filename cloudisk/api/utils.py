from pathlib import Path


def is_subpath(parent_path: Path, child_path: Path) -> bool:
    return parent_path.resolve() in child_path.resolve().parents
