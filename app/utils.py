import logging
from dataclasses import dataclass
from functools import cache
from pathlib import Path

from .constants import GIT_HEAD_FILE, GIT_OBJECTS_FOLDER
from .refs import GitRef

logger = logging.getLogger()


@cache
def gitignore() -> list[str]:
    path = Path(".gitignore")

    ignores = [".git"]
    if not path.is_file():
        return ignores

    gitignore_contents = (line.strip() for line in path.read_text().strip().splitlines())
    ignores.extend(line for line in gitignore_contents if not line.startswith("#"))
    return ignores


@dataclass
class ObjectPaths:
    folder: Path
    file: Path


def get_head_commit_path() -> ObjectPaths:
    branch = GIT_HEAD_FILE.read_text().strip()
    branch_ref_path = Path(branch.split(" ")[1]).relative_to("refs/heads")
    branch_ref = GitRef.from_name(str(branch_ref_path))
    return get_object_paths(branch_ref.commit_sha)


def get_object_paths(object_hash: str) -> ObjectPaths:
    if object_hash == "HEAD":
        return get_head_commit_path()

    folder_path = GIT_OBJECTS_FOLDER / object_hash[:2]
    file_path = folder_path / object_hash[2:]
    return ObjectPaths(folder=folder_path, file=file_path)
