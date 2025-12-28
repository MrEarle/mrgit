from pathlib import Path
from typing import ClassVar

from .base import BaseGitObject


class GitBlob(BaseGitObject):
    fmt: ClassVar = b"blob"
    file_contents: bytes

    @property
    def file_contents_str(self):
        return self.file_contents.decode()

    @classmethod
    def _deserialize_from_bytes(cls, content: bytes) -> "GitBlob":
        return GitBlob(file_contents=content)

    def _serialize_to_bytes(self) -> bytes:
        return self.file_contents

    @classmethod
    def build_from_file(cls, path: Path) -> "GitBlob":
        file_data = path.read_bytes()
        return GitBlob(file_contents=file_data)
