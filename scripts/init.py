import os
import subprocess

INFO = "\x1b[34mINFO\x1b[0m"

commands = [
    ("pipx install uv", "Installing uv"),
    ("uv sync", "Installing dependencies"),
    ("uv sync --group test", "Installing test dependencies"),
    ("pre-commit install", "Installing pre-commit hook"),
]

for command, text in commands:
    print(f"[{INFO}] {text} ({command})")  # noqa: T201
    subprocess.run(command.split(" "), check=True)

activate = (
    "source .venv/bin/activate" if os.name == "posix" else ".venv\\Scripts\\activate"
)

print(f"[{INFO}] Activate .venv with \x1b[32m{activate}\x1b[0m")  # noqa: T201
