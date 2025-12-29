from typing import Annotated

import typer
from rich.console import Console
from rich.text import Text

from app.constants import GIT_REFS_HEADS_FOLDER
from app.refs.ref import GitRef


def git_branch(
    name: Annotated[str | None, typer.Argument(help="Branch name, if creating branch")] = None,
):
    head = GitRef.from_head()
    if name is not None:
        GitRef(name=name, commit_sha=head.commit_sha).write_to_file()
        return

    all_branches = GIT_REFS_HEADS_FOLDER.rglob("*")
    console = Console()

    with console.pager(styles=True):
        for branch in all_branches:
            if branch.is_file():
                branch_name = branch.relative_to(GIT_REFS_HEADS_FOLDER)
                if str(branch_name) == head.name:
                    line = Text(f"(*) {branch_name!s}", "bold yellow")
                else:
                    line = Text(f"    {branch_name!s}")
                console.print(line)
