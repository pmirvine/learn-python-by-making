import os
import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest

type Commit = tuple[
    str, str
]  # a file's name, and the date, as 2026-03-02T10:00:00+00:00


def git(folder: Path, *arguments: str, when: str = "2026-01-01T00:00:00+00:00") -> None:
    """Run git as a made-up person, at a made-up time, so that tests are repeatable."""
    identity = {
        "GIT_AUTHOR_NAME": "A. Reader",
        "GIT_AUTHOR_EMAIL": "reader@example.com",
        "GIT_AUTHOR_DATE": when,
        "GIT_COMMITTER_NAME": "A. Reader",
        "GIT_COMMITTER_EMAIL": "reader@example.com",
        "GIT_COMMITTER_DATE": when,
    }
    subprocess.run(
        ["git", "-c", "commit.gpgsign=false", *arguments],
        cwd=folder,
        env=os.environ | identity,
        check=True,
        capture_output=True,
    )


@pytest.fixture
def make_project(tmp_path: Path) -> Callable[[str, list[Commit]], Path]:
    """Return a function that makes a project, with a history, in a folder of its own."""

    def make(name: str, commits: list[Commit]) -> Path:
        folder = tmp_path / name
        folder.mkdir()
        (folder / "pyproject.toml").write_text(f'[project]\nname = "{name}"\n')
        git(folder, "init", "--quiet", "--initial-branch=main")
        for file_name, when in commits:
            (folder / file_name).write_text(f"# written at {when}\n", encoding="utf-8")
            git(folder, "add", ".", when=when)
            git(folder, "commit", "--quiet", "-m", f"Add {file_name}", when=when)
        return folder

    return make
