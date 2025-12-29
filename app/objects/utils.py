from .base import BaseGitObject
from .blob import GitBlob
from .commit import GitCommit
from .tree import GitTree


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
