import logging
import zlib
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
    object_hash: str,
    pretty_print: Annotated[bool, typer.Option("--pretty-print", "-p", help="Pretty print <object> content")] = False,
):
    file_path = GIT_OBJECTS_FOLDER / object_hash[:2] / object_hash[2:]
    if not file_path.is_file():
        raise typer.Exit(1)

    compressed_content = file_path.read_bytes()
    file_contents = zlib.decompress(compressed_content)
    metadata, contents = file_contents.decode("utf-8").split("\0", 1)

    logger.info("Blob %s has metadata %s", object_hash, metadata)

    if pretty_print:
        print(contents, end="")


if __name__ == "__main__":
    app()
