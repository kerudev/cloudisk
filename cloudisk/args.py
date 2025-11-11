import argparse
from enum import StrEnum


class Command(StrEnum):
    INIT = "init"
    RUN = "run"

def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser(Command.INIT.value, help="Creates the basic configuration to run cloudisk")
    subparsers.add_parser(Command.RUN.value, help="Runs the cloudisk server on 127.0.0.1:8000")

    return parser.parse_args()