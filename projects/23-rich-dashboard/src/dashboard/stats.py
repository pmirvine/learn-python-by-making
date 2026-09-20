"""What there is to know about one project, and how to find it out."""

import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from dashboard import git

SKIP = {".venv", ".git", "__pycache__", "build", "dist", "site", "node_modules"}
TEST = re.compile(r"^\s*(?:async\s+)?def test_", re.MULTILINE)


@dataclass
class Project:
    name: str
    path: Path
    commits: list[datetime] = field(default_factory=list[datetime])
    branch: str = ""
    changed: int = 0
    lines: int = 0
    tests: int = 0

    @property
    def latest(self) -> datetime | None:
        return max(self.commits, default=None)

    @property
    def days_worked(self) -> int:
        """On how many different days was something committed?"""
        return len({commit.date() for commit in self.commits})


def python_files(folder: Path) -> list[Path]:
    """Return the project's own Python files, and not the ones it has installed."""
    return [
        path
        for path in folder.rglob("*.py")
        if not SKIP & set(path.relative_to(folder).parts)
    ]


def measure(folder: Path) -> tuple[int, int]:
    """Count the lines of Python in a folder that aren't blank, and the tests."""
    lines = tests = 0
    for path in python_files(folder):
        text = path.read_text(encoding="utf-8", errors="replace")
        lines += sum(1 for line in text.splitlines() if line.strip())
        tests += len(TEST.findall(text))
    return lines, tests


def scan(folder: Path) -> Project:
    """Find out everything about one project."""
    lines, tests = measure(folder)
    project = Project(folder.name, folder, lines=lines, tests=tests)
    if git.is_tracked(folder):
        project.commits = git.commit_times(folder)
        project.branch = git.branch(folder)
        project.changed = git.changed_files(folder)
    return project


def find_projects(root: Path) -> list[Path]:
    """Return the folders in `root` that look like Python projects, in order of name."""
    return sorted(
        folder
        for folder in root.iterdir()
        if folder.is_dir() and (folder / "pyproject.toml").is_file()
    )


def busiest_day(projects: list[Project]) -> str:
    """On which day of the week is the most work done?"""
    days = Counter(f"{commit:%A}" for project in projects for commit in project.commits)
    if not days:
        return "no day yet"
    (day, count), *_ = days.most_common(1)
    return f"{day}, with {count} commits"
