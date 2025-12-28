from typing import Annotated

import typer

from app.objects.commit import GitCommit


def git_log(sha: Annotated[str, typer.Argument(help="Sha of the commit to start logging from")]):
    current_sha: str | None = sha
    while current_sha:
        commit = GitCommit.from_object_hash(current_sha)
        print(commit.log_str())
        current_sha = commit.parent
