from cloudisk import logger, args, fs, server


def main():
    arguments = args.parse()

    match arguments.command:
        case args.Command.INIT.value:
            fs.init_file_structure()

        case args.Command.RUN.value:
            server.run_server()

        case _:
            logger.error(f"There is no command associated to {arguments.command}")


if __name__ == "__main__":
    main()
