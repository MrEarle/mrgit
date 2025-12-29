import logging

import typer

from .branch import git_branch
from .cat_file import git_cat_file
from .checkout import git_checkout
from .commit import git_commit
from .commit_tree import git_commit_tree
from .config import git_config
from .git_init import git_init
from .hash_object import git_hash_object
from .log import git_log
from .ls_tree import git_ls_tree
from .update_ref import git_update_ref
from .write_tree import git_write_tree

logging.basicConfig(
    format="%(message)s", handlers=[logging.FileHandler("mrgit.log")], level=logging.DEBUG
)
logger = logging.getLogger()


app = typer.Typer(no_args_is_help=True)


app.command(name="init")(git_init)
app.command(name="cat-file")(git_cat_file)
app.command(name="hash-object")(git_hash_object)
app.command(name="ls-tree")(git_ls_tree)
app.command(name="write-tree")(git_write_tree)
app.command(name="config")(git_config)
app.command(name="commit-tree")(git_commit_tree)
app.command(name="commit")(git_commit)
app.command(name="update-ref")(git_update_ref)
app.command(name="log")(git_log)
app.command(name="branch")(git_branch)
app.command(name="checkout")(git_checkout)


if __name__ == "__main__":
    app()
