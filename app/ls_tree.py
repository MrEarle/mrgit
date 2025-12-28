import logging
from typing import Annotated

import typer

from .constants import TreeEntry
from .utils import get_decompressed_object

logger = logging.getLogger()


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
        entry = TreeEntry(sha1=sha1.hex(), mode=int(mode.decode()), name=name.decode())  # ty:ignore[invalid-argument-type]  # pyright: ignore[reportArgumentType]
        print(entry.to_str(name_only))
