#!/bin/sh
#
# This script is used to run your program on CodeCrafters
#
# This runs after .codecrafters/compile.sh
#
# Learn more: https://codecrafters.io/program-interface

set -e # Exit on failure
ls -a
# uv sync
# uv pip list
exec uv run --with typer -m app.main "$@"
