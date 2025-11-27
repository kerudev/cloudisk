from cloudisk.cli.args import (
    PATH_FLAGS,
    Command,
    CommandName,
    Parser,
    RequiredFlag,
)
from cloudisk.fs.commands import init_cloudisk_folder, link_path, unlink_path
from cloudisk.http import server
from cloudisk.logger import get_logger
from cloudisk.vars import CLOUDISK_ROOT

logger = get_logger("cloudisk.parser")


def run():
    init = Command(
        name=CommandName.INIT,
        help=f"Creates the basic configuration to run cloudisk at '{CLOUDISK_ROOT}'",
        action=init_cloudisk_folder,
    )

    link = Command(
        name=CommandName.LINK,
        help=f"Creates a symlink inside {CLOUDISK_ROOT}",
        action=link_path,
        flags=[
            RequiredFlag(
                base=PATH_FLAGS,
                help=(
                    "If path is a file, creates a symlink to that file."
                    "If path is a dir, creates a symlink for each file/dir inside itself."
                ),
            ),
        ],
    )

    unlink = Command(
        name=CommandName.UNLINK,
        help=f"Removes a symlink inside {CLOUDISK_ROOT}",
        action=unlink_path,
        flags=[
            RequiredFlag(
                base=PATH_FLAGS,
                help="Path can refer to a file or dir",
            )
        ],
    )

    run = Command(
        name=CommandName.RUN,
        action=server.run,
        help="Runs the cloudisk server on 0.0.0.0:8000",
    )

    parser = Parser(
        name="cloudisk",
        description="A decentralized content distribution system. Run your own cloud.",
        commands=[
            init,
            link,
            unlink,
            run,
        ],
    )

    try:
        parser.dispatch()
    except Exception as e:
        logger.error(f"'{type(e).__name__}: {e}'")
