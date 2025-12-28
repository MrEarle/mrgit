import hashlib
import logging
import zlib
from pathlib import Path
from typing import Annotated

import typer

from .constants import GIT_OBJECTS_FOLDER, get_object_paths

logger = logging.getLogger()


def git_hash_object(
    file: str,
    write: Annotated[bool, typer.Option("--write", "-w", help=f"Write <object> to {GIT_OBJECTS_FOLDER}")] = False,
):
    file_path = Path(file)
    if not file_path.is_file():
        print(f"{file} is not a file")
        raise typer.Exit(1)

    file_contents = file_path.read_text()
    file_size = len(file_contents)

    blob_content = f"blob {file_size}\0{file_contents}".encode()
    blob_hash = hashlib.sha1(blob_content).hexdigest()

    print(blob_hash)

    if write:
        compressed_content = zlib.compress(blob_content)
        object_paths = get_object_paths(blob_hash)

        logger.info("Creating %s object folder if not exists", object_paths.folder)
        object_paths.file.mkdir(exist_ok=True)

        logger.info("Writing object to %s", object_paths.file)
        object_paths.file.write_bytes(compressed_content)
