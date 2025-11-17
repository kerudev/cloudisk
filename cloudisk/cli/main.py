from cloudisk.cli.args import Command, parse_args
from cloudisk.fs.commands import init_file_structure, link_path, unlink_path
from cloudisk.http import server
from cloudisk.logger import logger


def main():
    arguments = parse_args()

    match arguments.command:
        case Command.INIT:
            init_file_structure(arguments.path)

        case Command.LINK:
            link_path(arguments.path)

        case Command.UNLINK:
            unlink_path(arguments.path)

        case Command.RUN:
            server.run()

        case _:
            logger.error(f"There is no command associated to {arguments.command}")
