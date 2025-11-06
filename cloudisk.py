import logging
from cloudisk import args, fs

LOGGER = logging.getLogger("cloudisk.logger")

def main():
    arguments = args.parse()

    match arguments.command:
        case args.Command.INIT.value:
            fs.init_file_structure()

        case _:
            LOGGER.error(f"There is no command associated to {arguments.command}")


if __name__ == "__main__":
    main()
