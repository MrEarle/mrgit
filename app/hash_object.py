import logging
from pathlib import Path
from typing import Annotated

import typer

from app.utils import build_file_blob, write_hash_object

from .constants import GIT_OBJECTS_FOLDER

logger = logging.getLogger()


def git_hash_object(
    file: str,
    write: Annotated[bool, typer.Option("--write", "-w", help=f"Write <object> to {GIT_OBJECTS_FOLDER}")] = False,
):
    blob = build_file_blob(Path(file))

    print(blob.blob_hash)

    if write:
        write_hash_object(blob)
