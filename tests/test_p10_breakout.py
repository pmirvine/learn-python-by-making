"""Repo-level checks for Project 10: stage snapshots, and every program that opens a window.

The reader's own tests are in the project's tests/ folder.
"""

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("breakout", reason="needs the Project 10 environment")

P10 = Path(__file__).parent.parent / "projects" / "10-breakout"
HEADLESS = Path(__file__).parent / "headless.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_stage1_has_levels_but_no_bat_or_ball():
    model = load(P10 / "stages" / "stage1_model.py", "stage1_model")
    assert repr(model.Level.from_text("RR\n.#", "demo")) == "Level('demo', 3 bricks)"
    assert len(model.Level.built_in()) == 3
    assert not hasattr(model, "Ball")


def test_stage2_adds_the_bat_and_the_ball():
    model = load(P10 / "stages" / "stage2_model.py", "stage2_model")
    ball = model.Ball(5, 100)
    ball.speed = 200
    assert ball.vy == -200
    assert repr(model.Bat(model.Settings())) == "Bat(centre=160)"
    assert not hasattr(model, "Game")


def run_headless(program: Path, frames: int) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, HEADLESS, program, str(frames)],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )


@pytest.mark.parametrize("script", ["starfield.py", "solutions/bughunt/ball.py"])
def test_program_runs_for_thirty_frames(script):
    result = run_headless(P10 / script, 30)
    assert result.returncode == 0, result.stderr


def test_the_bug_hunt_crashes_as_the_chapter_says():
    result = run_headless(P10 / "bughunt" / "ball.py", 5)
    assert result.returncode != 0
    assert "RecursionError" in result.stderr


def test_the_game_itself_runs(tmp_path):
    program = tmp_path / "play.py"
    program.write_text("from breakout.app import main\n\nmain()\n", encoding="utf-8")
    result = run_headless(program, 30)
    assert result.returncode == 0, result.stderr
