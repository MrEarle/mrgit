from pathlib import Path
from typing import ClassVar, Literal

from pydantic import BaseModel, Field

from app.constants import TREE_MODE

from .base import BaseGitObject


class TreeEntry(BaseModel):
    sha1: str
    name: str
    mode: Literal[40000, 100644, 100755, 120000]

    @property
    def type(self):
        if self.mode == TREE_MODE:
            return "tree"
        return "blob"

    def to_str_representation(self, name_only=False):
        if name_only:
            return self.name

        return f"{self.mode:06d} {self.type} {self.sha1}\t{self.name}"

    def to_object_content(self):
        return f"{self.mode} {self.name}\0".encode() + bytes.fromhex(self.sha1)


class GitTree(BaseGitObject):
    fmt: ClassVar = b"tree"

    entries: list[TreeEntry] = Field(default_factory=list)

    def _serialize_to_bytes(self) -> bytes:
        return b"".join(e.to_object_content() for e in self.entries)

    @classmethod
    def _deserialize_from_bytes(cls, content: bytes) -> "GitTree":
        curr_content = content
        entries: list[TreeEntry] = []
        while curr_content:
            mode, rest = curr_content.split(b" ", maxsplit=1)
            name, rest = rest.split(b"\0", maxsplit=1)
            sha1, curr_content = rest[:20], rest[20:]
            entry = TreeEntry(
                sha1=sha1.hex(),
                mode=int(mode.decode()),  # ty:ignore[invalid-argument-type]
                name=name.decode(),
            )
            entries.append(entry)

        return GitTree(entries=entries)

    def get_payload(self, name_only=False) -> str:
        return "\n".join(entry.to_str_representation(name_only) for entry in self.entries)

    def get_paths_shas(self) -> dict[Path, TreeEntry]:
        path_shas: dict[Path, TreeEntry] = {}

        for entry in self.entries:
            path = Path(entry.name)
            path_shas[path] = entry

            if entry.type == "tree":
                subpath_shas = {
                    (path / p): s
                    for p, s in GitTree.from_object_hash(entry.sha1).get_paths_shas().items()
                }
                path_shas.update(subpath_shas)

        return path_shas
