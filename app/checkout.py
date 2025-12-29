from typing import Annotated

import typer

from app.checkout_utils.update_files import change_worktree


def git_checkout(name: Annotated[str, typer.Argument(help="Branch name to checkout")]):

    change_worktree(name)

    print(f"Checked out {name}")
