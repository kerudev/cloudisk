# cloudisk

[![Coverage Status](https://coveralls.io/repos/github/kerudev/cloudisk/badge.svg?branch=main)](https://coveralls.io/github/kerudev/cloudisk?branch=main)
[![Build Status](https://github.com/kerudev/cloudisk/workflows/Lint/badge.svg)](https://github.com/kerudev/cloudisk/actions)
[![PyPI - Version](https://img.shields.io/pypi/v/cloudisk)](https://pypi.org/project/cloudisk/)
[![PyPI - Python](https://img.shields.io/pypi/pyversions/cloudisk)](https://pypi.org/project/cloudisk/)


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

Cloudisk works with `spaces`, which are isolated server instances.
Run `cloudisk create` to make a new space.

Then, use `cloudisk run` to start the web server at `127.0.0.1:8000`.

If you want to use a different space, run `cloudisk use [NAME]`.

## Configuration

As mentioned before, cloudisk manages different server instances with spaces.

These spaces, the cloudisk database and the settings module are located in your
home directory:

- Linux: `$HOME/.cloudisk`
- macOS: `$HOME/.cloudisk`
- Windows: `%USERPROFILE%/.cloudisk`

The `.cloudisk` directory is created automatically, but you can also use
`cloudisk init` to generate it.

Right now, all spaces share the same database and settings module. In the
future, each space will have it's own settings module.

The settings module is just a Python file that contains some optional variables:
- `STATIC_PATH`: the path where the static files will be served from.
- `EMAIL_FROM`: the email of the account that sends the account verification email.
- `PASS_FROM`: the password of the account that sends the account verification email.

You can also set them up as environment variables by adding `CLOUDISK_` prefix
to the variable name. Eg.: `CLOUDISK_EMAIL_FROM`
