"""Repo-level checks for Project 19: the sample site, the bug hunt, and the extras.

The reader's own tests are in the project's tests/ folder.
"""

import runpy
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("pyfax", reason="needs the Project 19 environment")

P19 = Path(__file__).parent.parent / "projects" / "19-pyfax"
PYFAX = ("-c", "from pyfax.build import main; main()")  # what `uv run pyfax` does


def run(*arguments: str | Path, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *arguments],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=cwd,
        timeout=60,
        check=False,
    )


def test_the_sample_site_builds_from_the_command_line(tmp_path):
    result = run(*PYFAX, P19 / "content", "--out", "site", cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert result.stdout == "Wrote 5 pages to site/\n"
    names = sorted(path.name for path in (tmp_path / "site").iterdir())
    assert names == [
        "100.html", "101.html", "102.html", "301.html", "404.html", "501.html",
        "index.html", "pyfax.js", "style.css",
    ]  # fmt: skip


def test_a_folder_with_a_bad_article_is_reported_politely(tmp_path):
    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "bad.toml").write_text(
        'title = "No number"\n', encoding="utf-8"
    )
    result = run(*PYFAX, cwd=tmp_path)
    assert result.returncode == 1
    assert "Can't build the site: bad.toml needs a number" in result.stderr
    assert "Traceback" not in result.stderr


def test_the_bug_hunt_shows_its_symptom(tmp_path):
    result = run(P19 / "bughunt" / "dotty.py", cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    after = result.stdout.split("Out:\n")[1].splitlines()
    assert after[0] == "..#.#..."
    assert after[1] == "........"
    assert all(set(line) <= set("#.") for line in after)


def test_the_type_in_counts_in_binary(capsys):
    runpy.run_path(str(P19 / "sixels.py"), run_name="__main__")
    out = capsys.readouterr().out.splitlines()
    assert out[0].split() == [f"{n:06b}" for n in range(8)]
    assert out[1].split() == ["····", "██··", "··██", "████"] * 2
    assert out[-2].split()[-1] == "████"
    assert len(out) == 8 * 5


def test_the_publishing_workflow_builds_what_the_chapter_says():
    workflow = (P19 / ".github" / "workflows" / "publish.yml").read_text(
        encoding="utf-8"
    )
    assert "run: uv run pyfax content --out site" in workflow
    assert "actions/deploy-pages@" in workflow
    assert "pages: write" in workflow
