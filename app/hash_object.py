import logging
from pathlib import Path
from typing import Annotated

import typer

from .constants import GIT_OBJECTS_FOLDER
from .objects import GitBlob

logger = logging.getLogger()


def git_hash_object(
    file: str,
    write: Annotated[bool, typer.Option("--write", "-w", help=f"Write <object> to {GIT_OBJECTS_FOLDER}")] = False,
):
    blob = GitBlob.build_from_file(Path(file))

    print(blob.blob_hash)

    if write:
        blob.write_object()
