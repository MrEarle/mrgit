import logging
from typing import Annotated

import typer

from .objects import GitTree

logger = logging.getLogger()


def git_ls_tree(
    tree_hash: str,
    name_only: Annotated[
        bool, typer.Option("--name-only", help="Only output the name of the tree's entries.")
    ] = False,
):
    tree = GitTree.from_object_hash(tree_hash)
    print(tree.get_payload(name_only))
