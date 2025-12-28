import hashlib
import logging
import zlib
from abc import ABC, abstractmethod
from functools import cached_property
from typing import Literal

from pydantic import BaseModel

from app.constants import get_object_paths

GIT_OBJECT_TYPES = Literal["commit", "blob", "tree"]

logger = logging.getLogger()


class BaseGitObject(BaseModel, ABC):
    fmt: GIT_OBJECT_TYPES

    @abstractmethod
    def serialize_to_str(self) -> str: ...

    @classmethod
    @abstractmethod
    def deserialize_from_str(cls, data: str) -> "BaseGitObject": ...

    def serialize_to_bytes(self) -> bytes:
        return self.serialize_to_str().encode()

    @classmethod
    def deserialize_from_bytes(cls, data: bytes) -> "BaseGitObject":
        return cls.deserialize_from_str(data.decode())

    @cached_property
    def file_contents_str(self) -> str:
        content = self.serialize_to_str()
        return f"{self.fmt} {len(content)}\0{content}"

    @cached_property
    def file_contents_bytes(self) -> bytes:
        content = self.serialize_to_bytes()
        return f"{self.fmt} {len(content)}\0".encode() + content

    @cached_property
    def blob_hash(self):
        return hashlib.sha1(self.file_contents_bytes).hexdigest()

    def write_object(self):
        compressed_content = zlib.compress(self.file_contents_bytes)
        object_paths = get_object_paths(self.blob_hash)

        logger.info("Creating %s object folder if not exists", object_paths.folder)
        object_paths.folder.mkdir(exist_ok=True, parents=True)

        logger.info("Writing object to %s", object_paths.file)
        object_paths.file.write_bytes(compressed_content)
