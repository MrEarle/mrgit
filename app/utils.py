import contextlib
import logging
from dataclasses import dataclass
from functools import cache
from pathlib import Path

from .constants import GIT_OBJECTS_FOLDER
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


class EmptyRefError(Exception): ...


def get_branch_commit_path(name: str) -> ObjectPaths:
    try:
        ref = GitRef.from_head() if name == "HEAD" else GitRef.from_name(name)
    except FileNotFoundError:
        raise EmptyRefError from None

    if ref.commit_sha is None:
        raise EmptyRefError

    return get_object_paths(ref.commit_sha)


def get_object_paths(object_hash: str) -> ObjectPaths:
    with contextlib.suppress(EmptyRefError):
        return get_branch_commit_path(object_hash)

    folder_path = GIT_OBJECTS_FOLDER / object_hash[:2]
    file_path = folder_path / object_hash[2:]
    return ObjectPaths(folder=folder_path, file=file_path)
