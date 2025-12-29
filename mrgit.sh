#!/bin/sh
exec uv run --with typer -m app.main "$@"
