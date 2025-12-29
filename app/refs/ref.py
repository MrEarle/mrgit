from pathlib import Path

from pydantic import BaseModel

from app.constants import GIT_REFS_HEADS_FOLDER


class GitRef(BaseModel):
    name: str
    commit_sha: str

    @staticmethod
    def from_name(name: str) -> "GitRef":
        ref_file = GIT_REFS_HEADS_FOLDER / name
        commit_sha = ref_file.read_text()

        return GitRef(name=name, commit_sha=commit_sha)

    def write_to_file(self):
        from app.objects import GitCommit  # noqa: PLC0415

        # Check if the target commit is a valid commit
        GitCommit.from_object_hash(self.commit_sha)

        file = GIT_REFS_HEADS_FOLDER / Path(self.name)
        folder = file.parent
        folder.mkdir(parents=True, exist_ok=True)
        file.write_text(self.commit_sha)
