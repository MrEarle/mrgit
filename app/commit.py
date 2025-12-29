from typing import Annotated

import typer

from .commit_tree import commit_tree
from .constants import GIT_HEAD_FILE
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

    branch_ref = GIT_HEAD_FILE.read_text().strip()
    print(branch_ref)
    branch = branch_ref.removeprefix("ref: refs/heads/")
    print(branch)
    GitRef(name=branch, commit_sha=commit.blob_hash).write_to_file()
