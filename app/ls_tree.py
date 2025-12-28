import logging
from dataclasses import dataclass
from typing import Annotated

import typer

from .utils import get_decompressed_object

logger = logging.getLogger()

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


def git_ls_tree(
    tree_hash: str,
    name_only: Annotated[bool, typer.Option("--name-only", help="Only output the name of the tree's entries.")] = False,
):
    object_contents = get_decompressed_object(tree_hash)

    curr_content = object_contents.content
    while curr_content:
        mode, rest = curr_content.split(b" ", maxsplit=1)
        name, rest = rest.split(b"\0", maxsplit=1)
        sha1, curr_content = rest[:20], rest[20:]
        entry = TreeEntry(sha1=sha1.hex(), mode=int(mode.decode()), name=name.decode())
        print(entry.to_str(name_only))
