from dataclasses import dataclass
from pathlib import Path

GIT_FOLDER = Path(".git")
GIT_OBJECTS_FOLDER = GIT_FOLDER / "objects"
GIT_REFS_FOLDER = GIT_FOLDER / "refs"
GIT_HEAD_FILE = GIT_FOLDER / "HEAD"

TREE_MODE = 40000


@dataclass
class TreeEntry:
    sha1: str
    name: str
    mode: int

    @property
    def type(self):
        if self.mode == TREE_MODE:
            return "tree"
        return "blob"

    def to_str(self, name_only=False):
        if name_only:
            return self.name

        return f"{self.mode:6d} {self.type} {self.sha1}    {self.name}"


@dataclass
class ObjectPaths:
    folder: Path
    file: Path


def get_object_paths(object_hash: str) -> ObjectPaths:
    folder_path = GIT_OBJECTS_FOLDER / object_hash[:2]
    file_path = folder_path / object_hash[2:]
    return ObjectPaths(folder=folder_path, file=file_path)
