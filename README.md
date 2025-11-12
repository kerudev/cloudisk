# cloudisk

## Dependencies

Tools:
- Python >= 3.11
- uv >= 0.9.9

Libraries:
- fastapi >= 0.121.0
- sqlmodel >= 0.0.27
- uvicorn >= 0.38.0

Dev libraries:
- pre-commit >= 4.4.0
- pytest >= 8.4.2
- pytest-cov >= 7.0.0
- ruff >= 0.14.3

## Install dependencies

Quickstart with the following scripts:

```sh
./scripts/init.sh   // bash
./scripts/init.ps1  // powershell
./scripts/init.bat  // cmd
```

To install the dependencies in `pyproject.toml`, run:

```sh
uv sync
```

To install the `pre-commit` hook:

```sh
pre-commit install
```
