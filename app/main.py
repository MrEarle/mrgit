import logging

import typer

from .cat_file import git_cat_file
from .git_init import git_init
from .hash_object import git_hash_object
from .ls_tree import git_ls_tree

logging.basicConfig(format="%(message)s", handlers=[logging.FileHandler("mrgit.log")], level=logging.DEBUG)
logger = logging.getLogger()


app = typer.Typer(no_args_is_help=True)


app.command(name="init")(git_init)
app.command(name="cat-file")(git_cat_file)
app.command(name="hash-object")(git_hash_object)
app.command(name="ls-tree")(git_ls_tree)


if __name__ == "__main__":
    app()
