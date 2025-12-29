import logging
from typing import Annotated

import typer

from .objects import parse_any_object

logger = logging.getLogger()


def git_cat_file(
    object_hash: str,
    pretty_print: Annotated[bool, typer.Option("--pretty-print", "-p", help="Pretty print <object> content")] = False,
    show_object_type: Annotated[bool, typer.Option("--type", "-t", help="Show object type.")] = False,
):
    obj = parse_any_object(object_hash)

    if show_object_type:
        print(obj.fmt)

    if pretty_print:
        print(obj.get_payload())
