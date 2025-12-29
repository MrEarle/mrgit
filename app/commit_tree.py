import configparser
import logging
from datetime import UTC, datetime
from typing import Annotated

import typer

from .constants import GIT_CONFIG_FILE
from .objects import GitCommit, GitTree

logger = logging.getLogger()


def commit_tree(tree_sha: str, message: str, parent_sha: str | None) -> GitCommit:
    # Validate tree
    GitTree.from_object_hash(tree_sha)

    if parent_sha:
        # Validate parent
        GitCommit.from_object_hash(parent_sha)

    config = configparser.ConfigParser()
    config.read(GIT_CONFIG_FILE)

    try:
        user_name = config.get("user", "name")
    except (configparser.NoSectionError, configparser.NoOptionError):
        print("Missing user name. Run `config user.name <your name>` first.")
        raise typer.Exit(1) from None

    try:
        user_email = config.get("user", "email")
    except (configparser.NoSectionError, configparser.NoOptionError):
        print("Missing user email. Run `config user.email <your email>` first.")
        raise typer.Exit(1) from None

    timestamp = datetime.now(UTC)
    tz_offset = timestamp.strftime("%z")
    seconds_since_utc_epoch = int(timestamp.astimezone(UTC).timestamp())

    user = f"{user_name} <{user_email}> {seconds_since_utc_epoch} {tz_offset}"

    commit = GitCommit(author=user, committer=user, tree=tree_sha, parent=parent_sha, message=message)
    commit.write_object()

    return commit


def git_commit_tree(
    tree_sha: Annotated[str, typer.Argument(help="SHA1 of the tree to commit")],
    message: Annotated[str, typer.Option("--message", "-m", help="Message for the commit")],
    parent_sha: Annotated[str | None, typer.Option("--parent", "-p", help="SHA1 of the parent commit")] = None,
):
    commit = commit_tree(tree_sha, message, parent_sha)
    print(commit.blob_hash)
