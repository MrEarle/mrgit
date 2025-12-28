from typing import Annotated

import typer

from app.constants import get_ref_paths
from app.utils import get_decompressed_object


def git_update_ref(
    ref: Annotated[str, typer.Argument(help="Ref to update")],
    target_commit: Annotated[str, typer.Argument(help="Sha of the commit that the ref will point to")],
):
    commit_object = get_decompressed_object(target_commit)

    if commit_object.object_type != b"commit":
        print(f"{target_commit} is not a commit")
        raise typer.Exit(1)

    ref_paths = get_ref_paths(ref)
    print(ref_paths.file)
    ref_paths.folder.mkdir(parents=True, exist_ok=True)
    ref_paths.file.write_text(target_commit)
