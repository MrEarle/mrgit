import logging
from typing import Annotated

import typer

from app.ls_tree import git_ls_tree

from .utils import get_decompressed_object

logger = logging.getLogger()


def git_cat_file(
    object_hash: str,
    pretty_print: Annotated[bool, typer.Option("--pretty-print", "-p", help="Pretty print <object> content")] = False,
    show_object_type: Annotated[bool, typer.Option("--type", "-t", help="Show object type.")] = False,
):
    object_contents = get_decompressed_object(object_hash)
    logger.info("Blob %s has header %s", object_hash, object_contents.header)

    if show_object_type:
        print(object_contents.object_type)

    if pretty_print:
        if object_contents.object_type == b"tree":
            git_ls_tree(object_hash)
        else:
            print(object_contents.content.decode(), end="")
