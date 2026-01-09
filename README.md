# cloudisk

[![Coverage Status](https://coveralls.io/repos/github/kerudev/cloudisk/badge.svg?branch=main)](https://coveralls.io/github/kerudev/cloudisk?branch=main)
[![Build Status](https://github.com/kerudev/cloudisk/workflows/Lint/badge.svg)](https://github.com/kerudev/cloudisk/actions)

A decentralized content distribution system. Run your own cloud.

## Dependencies

Tools:
- Python >= 3.11
- uv >= 0.9.9

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

## Linting and formatting

We use `ruff` for linting and formatting, as well as `pre-commit` to run all
checks automatically before commits.

To execute `ruff`:

```sh
ruff check          # Checks formatting and linting rules defined in `pyproject.toml`
ruff check --fix    # Applies all safe lints
```

The `pre-commit` hook needs to be installed so it can be run automatically:

```sh
pre-commit install
```

In case you want to run `pre-commit` manually:

```sh
pre-commit run              # Runs just on staged changes
pre-commit run --all-files  # Runs on every file
```

## Testing

We use `pytest` to run out test suite and also upload our coverage to Coveralls
using `pytest-cov`.

To install the test dependencies:

```sh
uv sync --group test
```
