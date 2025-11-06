import argparse
from enum import StrEnum


class Command(StrEnum):
    INIT = "init"

def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser(Command.INIT.value, help="Creates the basic configuration to run cloudisk")

    return parser.parse_args()