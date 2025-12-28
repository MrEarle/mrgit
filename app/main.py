import hashlib
import logging
import zlib
from pathlib import Path
from typing import Annotated

import typer

from .constants import GIT_FOLDER, GIT_HEAD_FILE, GIT_OBJECTS_FOLDER, GIT_REFS_FOLDER

logging.basicConfig(format="%(message)s", handlers=[logging.FileHandler("mrgit.log")], level=logging.DEBUG)
logger = logging.getLogger()


app = typer.Typer(no_args_is_help=True)


@app.command(name="init")
def git_init():
    GIT_FOLDER.mkdir()
    GIT_OBJECTS_FOLDER.mkdir()
    GIT_REFS_FOLDER.mkdir()
    GIT_HEAD_FILE.write_text("ref: refs/heads/main\n")
    print("Initialized git directory")


@app.command(name="cat-file")
def git_cat_file(
    object_path: str,
    pretty_print: Annotated[bool, typer.Option("--pretty-print", "-p", help="Pretty print <object> content")] = False,
):
    file_path = GIT_OBJECTS_FOLDER / object_path[:2] / object_path[2:]
    if not file_path.is_file():
        print(f"{object_path} is not an existing blob")
        raise typer.Exit(1)

    compressed_content = file_path.read_bytes()
    file_contents = zlib.decompress(compressed_content)
    metadata, contents = file_contents.decode("utf-8").split("\0", 1)

    logger.info("Blob %s has metadata %s", object_path, metadata)

    if pretty_print:
        print(contents, end="")


@app.command(name="hash-object")
def git_hash_object(
    object_path: str,
    write: Annotated[bool, typer.Option("--write", "-w", help=f"Write <object> to {GIT_OBJECTS_FOLDER}")] = False,
):
    file_path = Path(object_path)
    if not file_path.is_file():
        print(f"{object_path} is not a file")
        raise typer.Exit(1)

    file_contents = file_path.read_text()
    file_size = len(file_contents)

    blob_content = f"blob {file_size}\0{file_contents}".encode()
    blob_hash = hashlib.sha1(blob_content).hexdigest()

    print(blob_hash)

    if write:
        compressed_content = zlib.compress(blob_content)
        blob_folder_path = GIT_OBJECTS_FOLDER / blob_hash[:2]
        blob_path = blob_folder_path / blob_hash[2:]
        logger.info("Creating %s object folder if not exists", blob_hash[:2])
        blob_folder_path.mkdir(exist_ok=True)

        logger.info("Writing object to %s", blob_path)
        blob_path.write_bytes(compressed_content)


if __name__ == "__main__":
    app()
