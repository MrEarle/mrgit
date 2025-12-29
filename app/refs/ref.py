from pathlib import Path

from pydantic import BaseModel

from app.constants import GIT_HEAD_FILE, GIT_REFS_HEADS_FOLDER


class GitRef(BaseModel):
    name: str
    commit_sha: str | None

    @staticmethod
    def from_name(name: str) -> "GitRef":
        ref_file = GIT_REFS_HEADS_FOLDER / name
        commit_sha = ref_file.read_text()

        return GitRef(name=name, commit_sha=commit_sha)

    @staticmethod
    def from_head() -> "GitRef":
        branch_ref = GIT_HEAD_FILE.read_text().strip()
        branch = branch_ref.removeprefix("ref: refs/heads/")
        try:
            return GitRef.from_name(branch)
        except FileNotFoundError:
            return GitRef(name=branch, commit_sha=None)

    def write_to_file(self):
        from app.objects import GitCommit  # noqa: PLC0415

        if self.commit_sha is None:
            return

        # Check if the target commit is a valid commit
        GitCommit.from_object_hash(self.commit_sha)

        file = GIT_REFS_HEADS_FOLDER / Path(self.name)
        folder = file.parent
        folder.mkdir(parents=True, exist_ok=True)
        file.write_text(self.commit_sha)
