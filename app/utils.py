import zlib
from dataclasses import dataclass

import typer

from .constants import get_object_paths


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


def get_decoded_object_contents(object_hash) -> ObjectContents:
    encoded_object = get_decompressed_object(object_hash)
    metadata = encoded_object.header.decode()
    contents = encoded_object.content.decode()
    return ObjectContents(header=metadata, content=contents)
