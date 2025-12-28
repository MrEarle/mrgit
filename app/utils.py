import logging
from functools import cache
from pathlib import Path

from .objects import BaseGitObject, GitBlob, GitCommit, GitTree

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


def parse_any_object(sha1: str) -> BaseGitObject:
    data = BaseGitObject.get_decompressed_data_from_hash(sha1)
    fmt, _ = data.split(b" ", maxsplit=1)

    match fmt:
        case b"tree":
            return GitTree.deserialize_from_bytes(data)
        case b"commit":
            return GitCommit.deserialize_from_bytes(data)
        case b"blob":
            return GitBlob.deserialize_from_bytes(data)
        case _:
            raise ValueError(f"Type {fmt} not supported")
