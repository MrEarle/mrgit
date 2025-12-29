from pathlib import Path

import typer

from app.constants import GIT_HEAD_FILE
from app.objects.blob import GitBlob
from app.objects.commit import GitCommit
from app.objects.tree import GitTree, TreeEntry
from app.refs.ref import GitRef


def all_paths_in_dir(directory: Path, ignores: list[str]):
    paths = []

    for path in directory.iterdir():
        if any(path.full_match(p) for p in ignores):
            continue

        if path.is_file():
            paths.append(path)

        if path.is_dir():
            paths.extend(all_paths_in_dir(path, ignores))

    return paths


def change_worktree(target_ref_name: str, dry_run=False):  # noqa: C901
    current_ref = GitRef.from_head()
    if current_ref.commit_sha is None:
        raise ValueError("No commits")

    if current_ref.name == target_ref_name:
        print("Checking out to current branch. No changes.")
        raise typer.Exit(0)

    current_commit = GitCommit.from_object_hash(current_ref.commit_sha)
    current_tree = GitTree.from_object_hash(current_commit.tree)
    current_paths = current_tree.get_paths_shas()

    target_ref = GitRef.from_name(target_ref_name)
    if target_ref.commit_sha is None:
        raise ValueError("Target branch has no commits")

    target_commit = GitCommit.from_object_hash(target_ref.commit_sha)
    target_tree = GitTree.from_object_hash(target_commit.tree)
    target_paths = target_tree.get_paths_shas()

    to_delete: dict[Path, TreeEntry] = {
        path: entry for path, entry in current_paths.items() if path not in target_paths
    }
    to_create: dict[Path, TreeEntry] = {
        path: entry for path, entry in target_paths.items() if path not in current_paths
    }
    to_overwrite: dict[Path, TreeEntry] = {
        path: entry
        for path, entry in target_paths.items()
        if ((entry_match := current_paths.get(path)) and entry_match.sha1 != entry.sha1)
    }

    common_paths = set(current_paths).intersection(target_paths)

    all_paths = (
        dict.fromkeys(to_delete, "delete")
        | dict.fromkeys(to_create, "create")
        | dict.fromkeys(to_overwrite, "overwrite")
        | {p: "keep" for p in common_paths if p not in to_overwrite}
    )

    for path, action in all_paths.items():
        print(f"{path!s:>40} -> {action}")
    if dry_run:
        return

    # 1. Update files
    dirs_to_delete: list[Path] = []
    for path, entry in to_delete.items():
        if entry.type == "tree":
            dirs_to_delete.append(path)
        else:
            path.unlink(missing_ok=True)

    for path in dirs_to_delete:
        path.rmdir()

    for path, entry in (to_create | to_overwrite).items():
        if entry.type == "tree":
            path.mkdir(exist_ok=True, parents=True)
        else:
            path.parent.mkdir(exist_ok=True, parents=True)
            file = GitBlob.from_object_hash(entry.sha1)
            path.write_bytes(file.file_contents)

    # 2. Change head
    GIT_HEAD_FILE.write_text(f"ref: refs/heads/{target_ref.name}")
