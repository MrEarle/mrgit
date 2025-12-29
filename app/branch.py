from typing import Annotated

import typer

from app.refs.ref import GitRef


def git_branch(name: Annotated[str, typer.Argument(help="Branch name")]):
    head = GitRef.from_head()
    GitRef(name=name, commit_sha=head.commit_sha).write_to_file()
