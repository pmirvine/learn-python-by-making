"""Repo-level checks for Project 12: the stage snapshot, and the programs that open a window.

The reader's own tests are in the project's tests/ folder.
"""

import importlib.util
import random
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("asteroids", reason="needs the Project 12 environment")

P12 = Path(__file__).parent.parent / "projects" / "12-asteroids"
HEADLESS = Path(__file__).parent / "headless.py"


def test_stage2_has_things_in_space_but_no_game():
    spec = importlib.util.spec_from_file_location(
        "stage2_model", P12 / "stages" / "stage2_model.py"
    )
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)

    rock = model.Rock(model.Vector(100, 100), model.Vector(), 3, random.Random(1))
    assert model.touching(rock, model.Zone(model.Vector(120, 100), 5))
    assert len(rock.split(random.Random(1))) == 2
    assert not hasattr(model, "Game")


def run_headless(program: Path, frames: int) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, HEADLESS, program, str(frames)],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )


def test_the_comet_runs():
    result = run_headless(P12 / "comet.py", 30)
    assert result.returncode == 0, result.stderr


def test_the_game_itself_runs(tmp_path):
    program = tmp_path / "play.py"
    program.write_text("from asteroids.app import main\n\nmain()\n", encoding="utf-8")
    result = run_headless(program, 30)
    assert result.returncode == 0, result.stderr


def test_the_bug_hunt_shows_its_symptom(play):
    out = play("12-asteroids/bughunt/fastvector.py", [])
    assert (
        "After shot 3:  the ship is at Vector(1660, 300), doing Vector(1260, -0)" in out
    )


def test_the_fixed_vector(play):
    out = play("12-asteroids/solutions/bughunt/fastvector.py", [])
    assert out.count("the ship is at Vector(400, 300), doing Vector(0, 0)") == 4
