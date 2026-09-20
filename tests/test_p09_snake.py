"""Repo-level checks for Project 9: the stage snapshot, and every program that opens a window.

The reader's own tests are in the project's tests/ folder.
"""

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("pygame", reason="needs the Project 9 environment")

P09 = Path(__file__).parent.parent / "projects" / "09-snake"
HEADLESS = Path(__file__).parent / "headless.py"


def test_stage1_has_a_snake_but_no_game():
    spec = importlib.util.spec_from_file_location(
        "stage1_model", P09 / "stages" / "stage1_model.py"
    )
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)

    snake = model.Snake((10, 5))
    snake.turn(model.Direction.DOWN)
    snake.advance()
    assert snake.head() == (10, 6)
    assert not hasattr(model, "Game")


@pytest.mark.parametrize(
    ("script", "frames"),
    [
        ("balls.py", 30),
        # With nobody steering, the two players meet head-on before long.
        ("bughunt/duel.py", 15),
        ("solutions/bughunt/duel.py", 15),
        ("solutions/two_player.py", 8),
    ],
)
def test_program_runs_for_a_while(script, frames):
    result = subprocess.run(
        [sys.executable, HEADLESS, P09 / script, str(frames)],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_the_game_itself_runs(tmp_path):
    program = tmp_path / "play.py"
    program.write_text("from snake.app import main\n\nmain()\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, HEADLESS, program, "30"],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stderr
