from .constants import (
    GIT_FOLDER,
    GIT_HEAD_FILE,
    GIT_OBJECTS_FOLDER,
    GIT_REFS_FOLDER,
    GIT_REFS_HEADS_FOLDER,
    GIT_REFS_TAGS_FOLDER,
)


def git_init():
    GIT_FOLDER.mkdir()
    GIT_OBJECTS_FOLDER.mkdir()
    GIT_REFS_FOLDER.mkdir()
    GIT_REFS_HEADS_FOLDER.mkdir()
    GIT_REFS_TAGS_FOLDER.mkdir()
    GIT_HEAD_FILE.write_text("ref: refs/heads/main")
    print("Initialized git directory")
