from typing import Annotated

import typer
from rich.console import Console

from app.objects.commit import GitCommit


def git_log(
    sha: Annotated[
        str, typer.Argument(help="Sha of a commit, or name of a branch, to start logging from")
    ] = "HEAD",
):
    current_sha: str | None = sha

    console = Console()
    with console.pager(styles=True):
        while current_sha:
            commit = GitCommit.from_object_hash(current_sha)
            console.print(commit.log_str())
            current_sha = commit.parent
