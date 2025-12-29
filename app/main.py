import logging
import os

import typer

from .branch import git_branch
from .cat_file import git_cat_file
from .checkout import git_checkout
from .commit import git_commit
from .commit_tree import git_commit_tree
from .config import git_config
from .git_init import git_init
from .hash_object import git_hash_object
from .log import git_log
from .ls_tree import git_ls_tree
from .update_ref import git_update_ref
from .write_tree import git_write_tree

logging.basicConfig(
    format="%(message)s", handlers=[logging.FileHandler("mrgit.log")], level=logging.DEBUG
)
logger = logging.getLogger()


app = typer.Typer(
    no_args_is_help=True,
)


COMPLEX_MODE = os.getenv("MRGIT_COMPLEX_MODE", "False").lower() == "true"


app.command(
    name="init",
    help="Initializes the repository. If the `.git` folder already exists, it fails.",
)(git_init)

app.command(
    name="config",
    help="Write git config.",
    no_args_is_help=True,
)(git_config)

app.command(
    name="log",
    help="Logs the entire commit history of the specified branch/commit",
)(git_log)

app.command(
    name="branch",
    help="Creates a new branch that points to the commit in the current HEAD.",
    no_args_is_help=True,
)(git_branch)

app.command(
    name="checkout",
    help=(
        "Updates all files in the current HEAD tree with the target branch's tree, "
        "and switches the HEAD to the target branch."
    ),
    no_args_is_help=True,
)(git_checkout)

app.command(
    name="commit",
    help="write-tree + commit-tree. Points to current HEAD as parent commit.",
    no_args_is_help=True,
)(git_commit)

if COMPLEX_MODE:
    app.command(
        name="cat-file",
        help="Reads an internal git object file, supports blob, tree and commit.",
        no_args_is_help=True,
    )(git_cat_file)

    app.command(
        name="hash-object",
        help="Gets the hash of a blob, and writes the blob to the objects folder if requested.",
        no_args_is_help=True,
    )(git_hash_object)

    app.command(
        name="ls-tree",
        help="Same as cat-file, but only works for tree objects.",
        no_args_is_help=True,
    )(git_ls_tree)

    app.command(
        name="write-tree",
        help=(
            "Creates a tree object with all of the workspace's current files, "
            "excluding paths specified in .gitignore."
        ),
        no_args_is_help=True,
    )(git_write_tree)

    app.command(
        name="commit-tree",
        help=(
            "Creates a commit object that points to a tree object. "
            "Optionally, also points to a parent commit."
        ),
        no_args_is_help=True,
    )(git_commit_tree)

    app.command(
        name="update-ref",
        help="Creates a ref that points to a commit.",
        no_args_is_help=True,
    )(git_update_ref)


if __name__ == "__main__":
    app()
