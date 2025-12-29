from typing import Annotated

import typer

from .commit_tree import commit_tree
from .objects import GitCommit
from .refs import GitRef
from .write_tree import write_tree


def git_commit(message: Annotated[str, typer.Option("--message", "-m", help="Commit message")]):
    entry = write_tree()

    try:
        parent_commit = GitCommit.from_object_hash("HEAD")
    except FileNotFoundError:
        parent_commit = None

    commit = commit_tree(
        tree_sha=entry.sha1,
        message=message,
        parent_sha=parent_commit.blob_hash if parent_commit is not None else None,
    )

    ref = GitRef.from_head()
    ref.commit_sha = commit.blob_hash
    ref.write_to_file()
