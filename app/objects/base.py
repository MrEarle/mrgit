import hashlib
import logging
import zlib
from abc import ABC, abstractmethod
from functools import cached_property
from typing import ClassVar, Literal, Self

from pydantic import BaseModel

from app.constants import get_object_paths

GIT_OBJECT_TYPES = Literal[b"commit", b"blob", b"tree"]

logger = logging.getLogger()


class BaseGitObject[T: GIT_OBJECT_TYPES](BaseModel, ABC):
    fmt: ClassVar[GIT_OBJECT_TYPES]

    def serialize_to_str(self) -> str:
        return self.serialize_to_bytes().decode()

    @classmethod
    def deserialize_from_str(cls, data: str) -> "BaseGitObject":
        return cls.deserialize_from_bytes(data.encode())

    def serialize_to_bytes(self) -> bytes:
        content = self._serialize_to_bytes()
        return self.fmt + f" {len(content)}".encode() + b"\0" + content

    @abstractmethod
    def _serialize_to_bytes(self) -> bytes: ...

    @classmethod
    def deserialize_from_bytes(cls, data: bytes) -> Self:
        header, content = data.split(b"\0", maxsplit=1)
        fmt, _ = header.split(b" ")
        if fmt != cls.fmt:
            raise ValueError(f"The data type {fmt} does not correspond to the type {cls.fmt}")
        return cls._deserialize_from_bytes(content)

    @classmethod
    @abstractmethod
    def _deserialize_from_bytes(cls, content: bytes) -> Self: ...

    @cached_property
    def file_contents_str(self) -> str:
        return self.serialize_to_str()

    @cached_property
    def file_contents_bytes(self) -> bytes:
        return self.serialize_to_bytes()

    @cached_property
    def blob_hash(self):
        return hashlib.sha1(self.file_contents_bytes).hexdigest()

    @classmethod
    def from_object_hash(cls, sha1: str) -> Self:
        return cls.deserialize_from_bytes(cls.get_decompressed_data_from_hash(sha1))

    def get_payload(self) -> str:
        return self._serialize_to_bytes().decode()

    def write_object(self):
        compressed_content = zlib.compress(self.file_contents_bytes)
        object_paths = get_object_paths(self.blob_hash)

        logger.info("Creating %s object folder if not exists", object_paths.folder)
        object_paths.folder.mkdir(exist_ok=True, parents=True)

        logger.info("Writing object to %s", object_paths.file)
        object_paths.file.write_bytes(compressed_content)

    @staticmethod
    def get_decompressed_data_from_hash(sha1: str) -> bytes:
        paths = get_object_paths(sha1)
        return zlib.decompress(paths.file.read_bytes())
