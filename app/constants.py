from dataclasses import dataclass
from pathlib import Path
from typing import Literal

GIT_FOLDER = Path(".git")
GIT_OBJECTS_FOLDER = GIT_FOLDER / "objects"
GIT_REFS_FOLDER = GIT_FOLDER / "refs"
GIT_HEAD_FILE = GIT_FOLDER / "HEAD"
GIT_CONFIG_FILE = GIT_FOLDER / "config"
TREE_MODE = 40000
FILE_MODE = 100644
EXEC_MODE = 100755
SYMLINK_MODE = 120000


@dataclass
class TreeEntry:
    sha1: str
    name: str
    mode: Literal[40000, 100644, 100755, 120000]

    @property
    def type(self):
        if self.mode == TREE_MODE:
            return "tree"
        return "blob"

    def to_str(self, name_only=False):
        if name_only:
            return self.name

        return f"{self.mode:06d} {self.type} {self.sha1}\t{self.name}"

    def to_object_content(self):
        return f"{self.mode} {self.name}\0".encode() + bytes.fromhex(self.sha1)


@dataclass
class ObjectPaths:
    folder: Path
    file: Path


def get_object_paths(object_hash: str) -> ObjectPaths:
    folder_path = GIT_OBJECTS_FOLDER / object_hash[:2]
    file_path = folder_path / object_hash[2:]
    return ObjectPaths(folder=folder_path, file=file_path)
