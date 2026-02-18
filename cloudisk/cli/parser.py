from pathlib import Path
from typing import Annotated, Optional

import typer

from cloudisk.cli.vars import HEADER_ART
from cloudisk.fs.commands import create_space, init_cloudisk_root, link_path, unlink_path
from cloudisk.http import server
from cloudisk.vars import CLOUDISK_ROOT

app = typer.Typer(
    name="cloudisk",
    help="A decentralized content distribution system. Run your own cloud.",
)


@app.command(help=f"Creates the basic scaffolding at '{CLOUDISK_ROOT}'")
def init():
    init_cloudisk_root()


@app.command(help=f"Creates a new space inside '{CLOUDISK_ROOT}'")
def create(
    name: Annotated[
        str,
        typer.Option("--name", "-n", help="Name of the instance."),
    ] = None,
    protect: Annotated[
        Optional[bool],
        typer.Option(
            "--protect",
            "-p",
            help="If `True`, all routes will be protected with user login.",
        ),
    ] = None,
):
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


@app.command(help=f"Creates a symlink inside '{CLOUDISK_ROOT}'")
def link(
    path: Annotated[
        Path,
        typer.Argument(
            help=(
                "If path is a file, creates a symlink to that file. "
                "If path is a dir, creates a symlink for each file/dir inside itself."
            ),
        ),
    ],
    recursive: Annotated[
        bool,
        typer.Option(
            "--recursive",
            "-r",
            help="If specified and path is a directory, it's contents are linked.",
        ),
    ] = False,
):
    link_path(path, recursive)


@app.command(help=f"Removes a symlink inside '{CLOUDISK_ROOT}'")
def unlink(
    path: Annotated[
        Path,
        typer.Argument(help="File or directory to unlink."),
    ],
):
    unlink_path(path)


@app.command(help="Runs the cloudisk server on 'host:port' (default: '0.0.0.0:8000')")
def run(
    host: Annotated[str, typer.Option()] = "0.0.0.0",
    port: Annotated[int, typer.Option()] = 8000,
):
    server.run(host=host, port=port)
