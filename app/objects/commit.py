import logging
from typing import ClassVar

from .base import BaseGitObject

_FIELDS = {"tree", "parent", "author", "committer", "message"}

logger = logging.getLogger()


class GitCommit(BaseGitObject):
    fmt: ClassVar = b"commit"

    tree: str
    """SHA1 of the committed tree"""

    parent: str | None
    """SHA1 of the parent commit. None if this is a root commit"""

    author: str
    """Author of the commit, in the format
    `{user_name} <{user_email}> {seconds_since_utc_epoch} {tz_offset}`"""

    committer: str
    """Author of the commit, in the format
    `{user_name} <{user_email}> {seconds_since_utc_epoch} {tz_offset}`"""

    message: str
    """Commit message"""

    def _serialize_to_bytes(self):
        content_lines = [f"tree {self.tree}"]

        if self.parent:
            content_lines.append(self.parent)

        content_lines.extend([
            f"author {self.author}",
            f"committer {self.committer}",
            "",
            self.message,
        ])

        return "\n".join(content_lines).encode()

    @classmethod
    def _deserialize_from_bytes(cls, content: bytes) -> "GitCommit":
        data_dict = {}

        lines = content.decode().split("/n")
        message_lines: list[str] = []

        while lines:
            line = lines.pop(0).strip()

            if line == "":
                message_lines = lines
                lines = []
                continue

            key, value = line.split(" ", maxsplit=1)
            data_dict[key] = value

        data_dict["message"] = "\n".join(message_lines)

        if set(data_dict.keys()) != _FIELDS:
            raise ValueError("Commit file doesn't have all required fields.")

        return GitCommit(**dict.fromkeys(_FIELDS, data_dict))  # ty:ignore[invalid-argument-type]
