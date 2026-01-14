import argparse
import os
import subprocess
import sys

RESET = "\x1b[0m"
GREEN = "\x1b[32m"
BLUE = "\x1b[34m"
INFO = f"{BLUE}INFO{RESET}"
ERR = f"\x1b[31mERR {RESET}"


if sys.prefix == sys.base_prefix:
    subprocess.run("uv venv --allow-existing -q".split(" "), check=True)
    activate = (
        "source .venv/bin/activate" if os.name == "posix" else ".venv\\Scripts\\activate"
    )

    print(f"[{ERR}] Please activate your virtualenv: {GREEN}{activate}{RESET}")  # noqa: T201
    exit(1)

parser = argparse.ArgumentParser()
parser.add_argument("--test", action="store_true")

arguments = parser.parse_args()

repository = "--repository testpypi" if arguments.test else ""
repository_name = "TestPyPI" if arguments.test else "PyPI"

commands = [
    ("uv sync --group build", "Installing build dependencies"),
    ("python -m build", "Generate 'dist' directory"),
    (
        f"twine upload {repository} dist/* --verbose",
        f"Upload package to {repository_name}",
    ),
]

for command, text in commands:
    print(f"[{INFO}] {text} {BLUE}({command}){RESET}")  # noqa: T201
    subprocess.run(command.split(" "), check=True)
