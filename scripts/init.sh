#!/usr/bin/env bash

pipx install uv
uv sync
pre-commit install
