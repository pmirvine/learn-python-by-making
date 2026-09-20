"""Repo-level checks for Project 16: the example programs, the bug hunt, and the extras.

The reader's own tests are in the project's tests/ folder.
"""

import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("logo", reason="needs the Project 16 environment")

from logo import Interpreter
from logo.turtle import Recorder

P16 = Path(__file__).parent.parent / "projects" / "16-logo"
HEADLESS = Path(__file__).parent / "headless.py"
LOGO = ("-c", "from logo.app import main; main()")  # what `uv run logo` does


def run(*arguments: str | Path, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *arguments],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=60,
        check=False,
        cwd=cwd,
    )


@pytest.mark.parametrize(("name", "lines"), [("tree", 511), ("spirograph", 144)])
def test_the_examples_draw_what_the_chapter_says(name, lines):
    canvas = Recorder()
    logo = Interpreter(canvas)
    logo.run((P16 / "examples" / f"{name}.logo").read_text(encoding="utf-8"))
    assert len(canvas.lines) == lines
    colours = {colour for _start, _end, colour in canvas.lines}
    assert len(colours) > 1


def test_the_tree_brings_the_turtle_back_to_where_it_started():
    logo = Interpreter(Recorder())
    logo.run((P16 / "examples" / "tree.logo").read_text(encoding="utf-8"))
    assert (round(logo.turtle.x, 6), round(logo.turtle.y, 6)) == (0, -200)


def test_the_bug_hunt_shows_its_symptom(tmp_path):
    result = run(P16 / "bughunt" / "lopsided.py", cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert "Drew 9 lines" in result.stdout
    assert "It's at -166, -12." in result.stdout
    assert (tmp_path / "lopsided.svg").read_text(encoding="utf-8").count("<line") == 9


def test_the_type_in_calculator(play):
    assert "[14.0]" in play("16-logo/rpn.py", ["3 4 + 2 *"])
    assert "[3.0, 20.0]" in play("16-logo/rpn.py", ["3 4 5 *"])


def test_drawing_to_a_file_from_the_command_line(tmp_path):
    picture = tmp_path / "tree.svg"
    result = run(*LOGO, P16 / "examples" / "tree.logo", "--svg", picture)
    assert result.returncode == 0, result.stderr
    assert "with 511 lines in it" in result.stdout
    assert picture.read_text(encoding="utf-8").startswith("<svg")


def test_a_bad_program_is_reported_and_not_a_traceback(tmp_path):
    program = tmp_path / "bad.logo"
    program.write_text("fd 100\njump 5\n", encoding="utf-8")
    result = run(*LOGO, program, "--svg", tmp_path / "bad.svg")
    assert result.returncode == 1
    assert "I don't know how to JUMP" in result.stderr
    assert "Traceback" not in result.stderr


def test_the_window_opens_and_runs_a_program(tmp_path):
    program = tmp_path / "play.py"
    example = P16 / "examples" / "spirograph.logo"
    program.write_text(
        "import sys\n"
        "from logo.app import main\n\n"
        f"sys.argv = ['logo', r'{example}']\n"
        "main()\n",
        encoding="utf-8",
    )
    result = run(HEADLESS, program, "10")
    assert result.returncode == 0, result.stderr
