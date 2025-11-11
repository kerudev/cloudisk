import argparse
from enum import StrEnum, auto
from pathlib import Path

from .fs import CLOUDISK_DIR

class Command(StrEnum):
    INIT = auto()
    LINK = auto()
    RUN = auto()

def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="cloudisk",
        description="Uncentralized content distribution system, on your own cloud",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser(Command.INIT.value, help="Creates the basic configuration to run cloudisk")
    init_parser.add_argument("--path", required=False, type=Path, default=Path.home() / CLOUDISK_DIR)

    subparsers.add_parser(Command.LINK.value, help="TODO")
    subparsers.add_parser(Command.RUN.value, help="Runs the cloudisk server on 0.0.0.0:8000")

    return parser.parse_args()