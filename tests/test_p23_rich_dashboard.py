"""Repo-level checks for Project 23: the bug hunt, the type-in, and the command itself.

The reader's own tests are in the project's tests/ folder.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("dashboard", reason="needs the Project 23 environment")

ROOT = Path(__file__).parent.parent
P23 = ROOT / "projects" / "23-rich-dashboard"
DASHBOARD = (
    "-c",
    "from dashboard.cli import main; main()",
)  # what `uv run dashboard` does


def run(*arguments: str | Path, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *arguments],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=cwd,
        env=os.environ | {"COLUMNS": "140", "PYTHONUTF8": "1"},
        timeout=120,
        check=False,
    )


def test_the_bug_hunt_shows_its_symptom():
    result = run(P23 / "bughunt" / "stale.py")
    assert result.returncode == 0, result.stderr
    assert "3 days, 0:05:00  ->  5 minutes ago" in result.stdout
    assert "400 days, 0:00:10  ->  just now" in result.stdout
    assert "2 days, 6:00:00  ->  2 days ago" in result.stdout


def test_the_dashboard_describes_the_tutorials_own_projects():
    result = run(*DASHBOARD, ROOT / "projects", "--sort", "name")
    assert result.returncode == 0, result.stderr
    assert "Sorted by name" in result.stdout
    assert "09-snake" in result.stdout
    assert "23-rich-dashboard" in result.stdout
    assert "projects" in result.stdout.splitlines()[-2]


def test_the_type_in_charts_a_repositorys_commits(tmp_path):
    git = [
        "git",
        "-c",
        "commit.gpgsign=false",
        "-c",
        "user.name=A",
        "-c",
        "user.email=a@b.c",
    ]
    subprocess.run([*git, "init", "--quiet"], cwd=tmp_path, check=True)
    for hour in (9, 9, 21):
        stamp = f"2026-03-02T{hour:02}:30:00+00:00"
        subprocess.run(
            [*git, "commit", "--quiet", "--allow-empty", "-m", "Work"],
            cwd=tmp_path,
            env=os.environ | {"GIT_AUTHOR_DATE": stamp, "GIT_COMMITTER_DATE": stamp},
            check=True,
        )
    result = run(P23 / "busy.py", cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    lines = result.stdout.splitlines()
    assert lines[9] == "09:00 " + "█" * 40 + " 2"
    assert lines[21] == "21:00 " + "█" * 20 + " 1"
    assert "Mon 3" in result.stdout
    assert "3 commits in 1 days, since 02 March 2026" in result.stdout
