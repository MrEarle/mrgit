import logging
from datetime import datetime
from functools import cached_property
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

    @cached_property
    def author_parts(self) -> list[str]:
        return self.author.split(" ")

    @cached_property
    def author_email(self) -> str:
        return self.author_parts[:-2][-1].strip("<").strip(">")

    @cached_property
    def author_name(self) -> str:
        return " ".join(self.author_parts[:-3])

    @cached_property
    def timestamp(self) -> str:
        tstamp = self.author_parts[-2]
        return datetime.fromtimestamp(int(tstamp)).strftime("%a %b %d %X %Y %z")

    def _serialize_to_bytes(self):
        content_lines = [f"tree {self.tree}"]

        if self.parent:
            content_lines.append(f"parent {self.parent}")

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

        lines = content.decode().split("\n")
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

        if "parent" not in data_dict:
            data_dict["parent"] = None

        if set(data_dict.keys()) != _FIELDS:
            raise ValueError("Commit file doesn't have all required fields.")

        return GitCommit(**data_dict)  # ty:ignore[invalid-argument-type]

    def log_str(self) -> str:
        lines = [
            f"commit {self.blob_hash}",
            f"Author {self.author_name} <{self.author_email}>",
            f"Date: {self.timestamp}",
            "",
            f"    {self.message.replace('\n', '\n    ')}",
            "",
        ]

        return "\n".join(lines)
