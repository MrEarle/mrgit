from typing import Annotated

import typer

from .constants import get_ref_paths
from .objects import GitCommit


def git_update_ref(
    ref: Annotated[str, typer.Argument(help="Ref to update")],
    target_commit: Annotated[str, typer.Argument(help="Sha of the commit that the ref will point to")],
):
    # Check if the target commit is a valid commit
    GitCommit.from_object_hash(target_commit)

    ref_paths = get_ref_paths(ref)
    ref_paths.folder.mkdir(parents=True, exist_ok=True)
    ref_paths.file.write_text(target_commit)
