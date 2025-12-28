import logging
import os
from pathlib import Path
from typing import Annotated

import typer

from .constants import EXEC_MODE, FILE_MODE, SYMLINK_MODE, TREE_MODE, TreeEntry
from .utils import ObjectBlob, build_file_blob, build_tree_blob, gitignore, write_hash_object

logger = logging.getLogger()


def _build_blob_entry(blob_path: Path) -> tuple[TreeEntry, list[ObjectBlob]]:
    blob = build_file_blob(blob_path)

    if blob_path.is_symlink():
        mode = SYMLINK_MODE
    elif os.access(blob_path, os.X_OK):
        # File is executable
        mode = EXEC_MODE
    else:
        mode = FILE_MODE

    logger.info("Writing blob for object %s with hash %s", blob_path, blob.blob_hash)
    # write_hash_object(blob)

    return TreeEntry(sha1=blob.blob_hash, name=blob_path.name, mode=mode), [blob]


def _build_tree_entry(tree_path: Path, ignores: list[str]) -> tuple[TreeEntry, list[ObjectBlob]]:
    if not tree_path.is_dir():
        raise typer.Exit(1)

    entries: list[TreeEntry] = []
    all_blobs: list[ObjectBlob] = []
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
    blob = build_tree_blob(tree_path, contents)
    all_blobs.append(blob)

    logger.info("Built tree object with contents %s", contents)
    logger.info("Writing blob for tree %s with hash %s", tree_path, blob.blob_hash)
    # write_hash_object(blob)

    return TreeEntry(
        sha1=blob.blob_hash,
        name=tree_path.name,
        mode=TREE_MODE,
    ), all_blobs


def git_write_tree(dry_run: Annotated[bool, typer.Option("--dry-run", help="Does not write anything in disk")] = False):
    entry, blobs = _build_tree_entry(Path.cwd(), gitignore())

    for blob in blobs:
        logger.info("%sWriting %s object of path %s", "[Dry Run] " if dry_run else "", blob.type, blob.path)
        if not dry_run:
            write_hash_object(blob)

    print(entry.sha1)
