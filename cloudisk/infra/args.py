import argparse
from enum import StrEnum, auto
from pathlib import Path

from fs import CLOUDISK_ROOT

PATH_FLAGS = ("-p", "--path")


class Command(StrEnum):
    INIT = auto()
    LINK = auto()
    UNLINK = auto()
    RUN = auto()


def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="cloudisk",
        description="Uncentralized content distribution system, on your own cloud",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser(
        Command.INIT.value, help="Creates the basic configuration to run cloudisk"
    )
    init_parser.add_argument(*PATH_FLAGS, type=Path, default=CLOUDISK_ROOT, help="")

    link_parser = subparsers.add_parser(
        Command.LINK.value, help=f"Creates a symlink inside {CLOUDISK_ROOT}"
    )
    link_parser.add_argument(
        *PATH_FLAGS,
        type=Path,
        required=True,
        help=(
            "If path is a file, creates a symlink to that file."
            "If path is a dir, creates a symlink for each file/dir inside itself."
        ),
    )

    unlink_parser = subparsers.add_parser(
        Command.UNLINK.value, help=f"Removes a symlink inside {CLOUDISK_ROOT}"
    )
    unlink_parser.add_argument(*PATH_FLAGS, type=Path)
    subparsers.add_parser(
        Command.RUN.value, help="Runs the cloudisk server on 0.0.0.0:8000"
    )

    return parser.parse_args()
