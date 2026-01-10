# cloudisk

[![Coverage Status](https://coveralls.io/repos/github/kerudev/cloudisk/badge.svg?branch=main)](https://coveralls.io/github/kerudev/cloudisk?branch=main)
[![Build Status](https://github.com/kerudev/cloudisk/workflows/Lint/badge.svg)](https://github.com/kerudev/cloudisk/actions)
[![PyPI - Version](https://img.shields.io/pypi/v/cloudisk?label=version)](https://pypi.org/project/cloudisk/)
[![PyPI - Python](https://img.shields.io/pypi/pyversions/cloudisk?label=python)](https://pypi.org/project/cloudisk/)

> [!WARNING]
> This library is still on a pre-alpha state.
> Keep your eyes open for future releases!

A decentralized content distribution system. Run your own cloud.

## The idea

cloudisk is born from the need of a simple server to share pictures and videos
with friends that doesn't depend on file size or device storage.

We decided to program our own, kind of like CLI `Jellyfin`, where we can add
the features we need: an intuitive and private cloud that is easy to use and
easy to develop.

## Getting started

To install cloudisk, use `pip install cloudisk`.

After installing, you can run `cloudisk -h` to get the full commands list and
a their description. Use `cloudisk <command> -h` to get help about their flags.

Use `cloudisk run` to start the web server at `127.0.0.1:8000`.
