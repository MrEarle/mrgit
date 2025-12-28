import hashlib
import logging
import zlib
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Literal

import typer

from .constants import get_object_paths

logger = logging.getLogger()


@dataclass
class ObjectContents:
    header: str
    content: str

    @property
    def object_type(self):
        return self.header.split(" ")[0]

    @property
    def object_size(self):
        return self.header.split(" ")[1]


@dataclass
class EncodedObjectContents:
    header: bytes
    content: bytes

    @property
    def object_type(self):
        return self.header.split(b" ")[0]

    @property
    def object_size(self):
        return self.header.split(b" ")[1]


def get_decompressed_object(object_hash) -> EncodedObjectContents:
    object_paths = get_object_paths(object_hash)
    if not object_paths.file.is_file():
        print(f"{object_hash} is not an existing blob")
        raise typer.Exit(1)

    compressed_content = object_paths.file.read_bytes()
    file_contents = zlib.decompress(compressed_content)
    header, contents = file_contents.split(b"\0", maxsplit=1)

    return EncodedObjectContents(header=header, content=contents)


@dataclass
class ObjectBlob:
    type: Literal["tree", "blob"]
    content: bytes
    path: Path

    @cached_property
    def size(self):
        return len(self.content)

    @cached_property
    def blob_hash(self):
        return hashlib.sha1(self.content).hexdigest()

    @cached_property
    def decoded_content(self):
        decoded = self.content.decode()
        decoded_size = len(decoded)

        return ObjectContents(header=f"blob {decoded_size}", content=decoded)


def build_file_blob(file_path: Path) -> ObjectBlob:
    if not file_path.is_file():
        logger.error("%s is not a file", file_path)
        raise typer.Exit(1)

    file_contents = file_path.read_bytes()
    file_size = len(file_contents)

    blob_content = f"blob {file_size}\0".encode() + file_contents

    return ObjectBlob(content=blob_content, type="blob", path=file_path)


def build_tree_blob(dir_path: Path, contents: bytes) -> ObjectBlob:
    content_size = len(contents)

    return ObjectBlob(type="tree", content=f"tree {content_size}\0".encode() + contents, path=dir_path)


def write_hash_object(blob: ObjectBlob):
    compressed_content = zlib.compress(blob.content)
    object_paths = get_object_paths(blob.blob_hash)

    logger.info("Creating %s object folder if not exists", object_paths.folder)
    object_paths.folder.mkdir(exist_ok=True, parents=True)

    logger.info("Writing object to %s", object_paths.file)
    object_paths.file.write_bytes(compressed_content)


def gitignore() -> list[str]:
    path = Path(".gitignore")

    ignores = [".git"]
    if not path.is_file():
        return ignores

    gitignore_contents = (line.strip() for line in path.read_text().strip().splitlines())
    ignores.extend(line for line in gitignore_contents if not line.startswith("#"))
    return ignores
