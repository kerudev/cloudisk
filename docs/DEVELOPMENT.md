# Guide for developers

This document will guide you on how to install cloudisk's dependencies and how
to use them. Keep in mind this document can change as the project grows and you
may need to reinstall your virtual environment.

## Install dependencies

The Python minor supported version is `3.10`, but newer versions are preferred.

The package manager we use is `uv >= 0.9.9`. It can manage dependencies, Python
versions and virtual envs.

Quickstart with the following scripts:

```sh
python ./scripts/init.py   # Works on all OS
```

To install the dependencies in `pyproject.toml`, run:

```sh
uv sync                     # Installs dependencies and dev
uv sync --group test        # Installs dependencies, dev and test
```

## Linting and formatting

We use `ruff` for linting and formatting, as well as `pre-commit` to run all
checks automatically before commits.

To execute `ruff`:

```sh
ruff check          # Checks formatting and linting rules defined in pyproject.toml
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

You can check the current coverage [here](https://coveralls.io/github/kerudev/cloudisk?branch=main).

## Uploading to PyPI

To upload to PyPI, you'll need to activate your virtual env, then run:

```sh
python scripts/upload.py --test  # Upload project to TestPyPI (optional)
python scripts/upload.py         # Upload project to PyPI
```
