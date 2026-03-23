from pathlib import Path
from typing import Annotated, Optional

import typer

from cloudisk.cli.vars import HEADER_ART
from cloudisk.vars import CLOUDISK_ROOT, VERSION

app = typer.Typer(
    name="cloudisk",
    help="A decentralized content distribution system. Run your own cloud.",
)


def version_cb(value: bool):
    if value:
        version = ".".join(str(x) for x in VERSION)
        typer.echo(f"cloudisk v{version}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            "-v",
            help="Print the version number",
            callback=version_cb,
            is_eager=True,
        ),
    ] = None,
):
    pass


@app.command(help=f"Creates the basic scaffolding at '{CLOUDISK_ROOT}'")
def init():
    from cloudisk.fs.commands import init_cloudisk_root

    init_cloudisk_root()


@app.command(help=f"Creates a new space inside '{CLOUDISK_ROOT}'")
def create(
    name: Annotated[
        Optional[str],
        typer.Argument(
            help=(
                "Name of the instance. "
                "If this is the first created space, it's used by default."
            )
        ),
    ] = None,
    protect: Annotated[
        Optional[bool],
        typer.Option(
            "--protect",
            "-p",
            help="If 'True', all routes will be protected with user login.",
        ),
    ] = None,
):
    from cloudisk.fs.commands import create_space

    typer.echo(HEADER_ART)

    prompt_name = "> Name of the space"

    if not name:
        name = typer.prompt(prompt_name)
    else:
        typer.echo(f"{prompt_name}: {name}")

    prompt_protect = "> Protect routes with user login?"

    if protect is None:
        protect = typer.confirm(prompt_protect)
    else:
        selected = "Y" if protect else "N"
        typer.echo(f"{prompt_protect} [Y/N] {selected}")

    create_space(name, protect)


@app.command(help=f"Changes the used space to one inside '{CLOUDISK_ROOT}'")
def use(
    name: Annotated[
        str,
        typer.Argument(help="Name of the space."),
    ],
):
    from cloudisk.fs.commands import use_space

    use_space(name)


@app.command(help=f"Lists all tracked spaces inside '{CLOUDISK_ROOT}'")
def list():
    from cloudisk.fs.commands import list_spaces

    list_spaces()


@app.command(help=f"Creates a (soft) symlink inside '{CLOUDISK_ROOT}'")
def link(
    path: Annotated[
        Path,
        typer.Argument(help="File or directory to link."),
    ],
    recursive: Annotated[
        bool,
        typer.Option(
            "--recursive",
            "-r",
            help="If path is a directory, the contents inside it are linked.",
        ),
    ] = False,
):
    from cloudisk.fs.commands import link_path

    link_path(path, recursive)


@app.command(help=f"Removes a (soft) symlink inside '{CLOUDISK_ROOT}'")
def unlink(
    path: Annotated[
        Path,
        typer.Argument(help="File or directory to unlink."),
    ],
):
    from cloudisk.fs.commands import unlink_path

    unlink_path(path)


@app.command(help="Runs the server on 'host:port' (default: '0.0.0.0:8000')")
def run(
    host: Annotated[str, typer.Option(help="Host of the server")] = "0.0.0.0",
    port: Annotated[int, typer.Option(help="Port of the server")] = 8000,
):
    from cloudisk.http import server

    server.run(host=host, port=port)
