@echo off
setlocal

pipx install uv
uv sync
pre-commit install

endlocal
