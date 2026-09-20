"""Repo-level checks for Project 24: the type-in, the bug hunt, and the command line.

The reader's own tests, snapshots among them, are in the project's tests/ folder.
"""

import re
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("teleview", reason="needs the Project 24 environment")

P24 = Path(__file__).parent.parent / "projects" / "24-teletext-viewer"
TELEVIEW = (
    "-c",
    "from teleview.app import main; main()",
)  # what `uv run teleview` does


def run(*arguments: str | Path, cwd: Path = P24) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *arguments],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=cwd,
        timeout=60,
        check=False,
    )


def test_the_type_in_descriptor_notices_changes():
    result = run(P24 / "watched.py")
    assert result.returncode == 0, result.stderr
    first, second = result.stdout.splitlines()
    assert first == "Retuning from 1 to 4"
    assert re.fullmatch(
        r"4 \{'channel': 4\} <__main__\.Watched object at 0x[0-9a-fA-F]+>", second
    )


def test_the_bug_hunt_shows_both_of_its_symptoms():
    result = run(P24 / "bughunt" / "breadcrumbs.py")
    assert result.returncode == 0, result.stderr
    assert "Went to 500.  Trail: 100\n" in result.stdout
    assert result.stdout.rstrip().endswith("[100, 101, 301, 500]")


def test_the_command_line_offers_the_three_ways_of_drawing():
    result = run(*TELEVIEW, "--help")
    assert result.returncode == 0
    assert "{braille,quadrant,sextant}" in result.stdout


def test_a_folder_with_nothing_in_it_is_reported_politely(tmp_path):
    result = run(*TELEVIEW, tmp_path / "nowhere")
    assert result.returncode == 1
    assert "Can't read the pages" in result.stderr
    assert "Traceback" not in result.stderr


def test_there_are_four_snapshots_and_they_are_pictures():
    snapshots = sorted((P24 / "tests" / "__snapshots__").rglob("*.raw"))
    assert len(snapshots) == 4
    assert all("<svg" in path.read_text(encoding="utf-8") for path in snapshots)
