import logging
import zlib
from typing import Annotated

import typer

from .constants import get_object_paths

logger = logging.getLogger()


def git_cat_file(
    object_hash: str,
    pretty_print: Annotated[bool, typer.Option("--pretty-print", "-p", help="Pretty print <object> content")] = False,
):
    object_paths = get_object_paths(object_hash)
    if not object_paths.file.is_file():
        print(f"{object_hash} is not an existing blob")
        raise typer.Exit(1)

    compressed_content = object_paths.file.read_bytes()
    file_contents = zlib.decompress(compressed_content)
    metadata, contents = file_contents.decode("utf-8").split("\0", 1)

    logger.info("Blob %s has metadata %s", object_hash, metadata)

    if pretty_print:
        print(contents, end="")
