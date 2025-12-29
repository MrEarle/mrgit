import logging
import os
from pathlib import Path
from typing import Annotated

import typer

from .constants import EXEC_MODE, FILE_MODE, SYMLINK_MODE, TREE_MODE
from .objects import GitBlob, GitTree, TreeEntry
from .utils import gitignore

logger = logging.getLogger()


def _build_blob_entry(blob_path: Path) -> tuple[TreeEntry, list[GitBlob]]:
    blob = GitBlob.build_from_file(blob_path)

    if blob_path.is_symlink():
        mode = SYMLINK_MODE
    elif os.access(blob_path, os.X_OK):
        # File is executable
        mode = EXEC_MODE
    else:
        mode = FILE_MODE

    return TreeEntry(sha1=blob.blob_hash, name=blob_path.name, mode=mode), [blob]


def _build_tree_entry(
    tree_path: Path, ignores: list[str]
) -> tuple[TreeEntry, list[GitBlob | GitTree]]:
    if not tree_path.is_dir():
        raise typer.Exit(1)

    entries: list[TreeEntry] = []
    all_blobs: list[GitBlob | GitTree] = []
    for child_path in tree_path.iterdir():
        if any(child_path.relative_to(Path.cwd()).full_match(p) for p in ignores):
            continue

        if child_path.is_file():
            e, b = _build_blob_entry(child_path)
        else:
            e, b = _build_tree_entry(child_path, ignores)
        entries.append(e)
        all_blobs.extend(b)

    entries.sort(key=lambda e: e.name)

    contents = b"".join(entry.to_object_content() for entry in entries)
    blob = GitTree(entries=entries)
    for entry in blob.entries:
        print(entry.to_str_representation())
    all_blobs.append(blob)

    logger.info("Built tree object with contents %s", contents)

    return TreeEntry(
        sha1=blob.blob_hash,
        name=tree_path.name,
        mode=TREE_MODE,
    ), all_blobs


def write_tree(dry_run: bool = False) -> TreeEntry:
    entry, blobs = _build_tree_entry(Path.cwd(), gitignore())

    for blob in blobs:
        logger.info(
            "%sWriting %s object with hash %s",
            "[Dry Run] " if dry_run else "",
            blob.fmt,
            blob.blob_hash,
        )
        if not dry_run:
            blob.write_object()

    return entry


def git_write_tree(
    dry_run: Annotated[
        bool, typer.Option("--dry-run", help="Does not write anything in disk")
    ] = False,
):
    entry = write_tree(dry_run)

    print(entry.sha1)
