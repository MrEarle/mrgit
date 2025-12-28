from dataclasses import dataclass
from pathlib import Path

GIT_FOLDER = Path(".git")
GIT_OBJECTS_FOLDER = GIT_FOLDER / "objects"
GIT_REFS_FOLDER = GIT_FOLDER / "refs"
GIT_HEAD_FILE = GIT_FOLDER / "HEAD"


@dataclass
class ObjectPaths:
    folder: Path
    file: Path


def get_object_paths(object_hash: str):
    folder_path = GIT_OBJECTS_FOLDER / object_hash[:2]
    file_path = folder_path / object_hash[2:]
    return ObjectPaths(folder=folder_path, file=file_path)
