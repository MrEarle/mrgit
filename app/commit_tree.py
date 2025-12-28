import configparser
import logging
from datetime import UTC, datetime
from typing import Annotated

import typer

from app.constants import GIT_CONFIG_FILE

from .utils import ObjectBlob, get_decompressed_object, write_hash_object

logger = logging.getLogger()


def git_commit_tree(
    tree_sha: Annotated[str, typer.Argument(help="SHA1 of the tree to commit")],
    message: Annotated[str, typer.Option("--message", "-m", help="Message for the commit")],
    parent_sha: Annotated[str | None, typer.Option("--parent", "-p", help="SHA1 of the parent commit")] = None,
):
    lines = [f"tree {tree_sha}"]

    if parent_sha:
        parent_object = get_decompressed_object(parent_sha)
        if parent_object.object_type != b"tree":
            logger.error("%s is not a tree.", parent_sha)
            raise typer.Exit(1)

        lines.append(f"parent {parent_sha}")

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
    lines.append(f"author {user}")
    lines.append(f"committer {user}")
    lines.append("")
    lines.append(message)

    content = "\n".join(lines)
    full_object = f"commit {len(content)}\0{content}"

    blob = ObjectBlob(type="commit", content=full_object.encode())
    write_hash_object(blob)

    print(blob.blob_hash)
