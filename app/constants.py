from dataclasses import dataclass
from pathlib import Path

GIT_FOLDER = Path(".git")
GIT_OBJECTS_FOLDER = GIT_FOLDER / "objects"
GIT_REFS_FOLDER = GIT_FOLDER / "refs"
GIT_REFS_HEADS_FOLDER = GIT_REFS_FOLDER / "heads"
GIT_REFS_TAGS_FOLDER = GIT_REFS_FOLDER / "tags"
GIT_HEAD_FILE = GIT_FOLDER / "HEAD"
GIT_CONFIG_FILE = GIT_FOLDER / "config"
TREE_MODE = 40000
FILE_MODE = 100644
EXEC_MODE = 100755
SYMLINK_MODE = 120000


@dataclass
class ObjectPaths:
    folder: Path
    file: Path


def get_object_paths(object_hash: str) -> ObjectPaths:
    folder_path = GIT_OBJECTS_FOLDER / object_hash[:2]
    file_path = folder_path / object_hash[2:]
    return ObjectPaths(folder=folder_path, file=file_path)


def get_ref_paths(ref: str) -> ObjectPaths:
    file_path = GIT_FOLDER / Path(ref)
    folder = file_path.parent

    return ObjectPaths(folder=folder, file=file_path)
