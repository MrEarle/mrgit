import configparser

import typer

from app.constants import GIT_CONFIG_FILE


def git_config(
    key: str = typer.Argument(help="Config key"),
    value: str = typer.Argument(help="Value to store in the key"),
):
    config = configparser.ConfigParser()
    config.read(GIT_CONFIG_FILE)

    section, key = key.split(".")

    if section not in config:
        config.add_section(section)

    config.set(section, key, value)

    with GIT_CONFIG_FILE.open("w") as f:
        config.write(f)
