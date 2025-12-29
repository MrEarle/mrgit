from typing import Annotated

import typer

from app.constants import GIT_HEAD_FILE
from app.refs.ref import GitRef


def git_checkout(name: Annotated[str, typer.Argument(help="Branch name to checkout")]):
    # Ensure ref exists
    ref = GitRef.from_name(name)
    if ref.commit_sha is None:
        print(f"Branch {ref.name} does not exist.")
        raise typer.Exit(1)

    GIT_HEAD_FILE.write_text(f"ref: refs/heads/{ref.name}")

    print(f"Checked out {ref.name}")
