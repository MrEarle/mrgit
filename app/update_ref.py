from typing import Annotated

import typer

from .refs import GitRef


def git_update_ref(
    ref: Annotated[str, typer.Argument(help="Ref to update")],
    target_commit: Annotated[str, typer.Argument(help="Sha of the commit that the ref will point to")],
):
    GitRef(name=ref, commit_sha=target_commit).write_to_file()
