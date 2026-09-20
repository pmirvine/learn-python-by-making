"""Repo-level checks for Project 8: the parts a reader's own tests don't cover.

Run inside the project's environment, from the repository root:

    uv run --project projects/08-mode2-sketchpad pytest tests/test_p08_sketchpad.py
"""

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("pygame", reason="needs the Project 8 environment")
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

P08 = Path(__file__).parent.parent / "projects" / "08-mode2-sketchpad"
HEADLESS = Path(__file__).parent / "headless.py"

pytestmark = pytest.mark.filterwarnings("ignore:no fast renderer available")


def load(path: Path, name: str):
    """Import a Python file that isn't on the import path, under the given name."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    "script",
    [
        "examples/window.py",
        "examples/moire_raw.py",
        "examples/moire.py",
        "examples/lines.py",
        "examples/paint.py",
        "examples/strings.py",
        "stages/stage5_paint_first_try.py",
        "bughunt/lines.py",
        "solutions/bughunt/lines.py",
        "solutions/lines_mirror.py",
        "solutions/paint.py",
    ],
)
def test_program_runs_for_a_hundred_frames(script):
    result = subprocess.run(
        [sys.executable, HEADLESS, P08 / script, "100"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr


def test_the_test_card_runs(tmp_path):
    program = tmp_path / "test_card.py"
    program.write_text("import beeb\n\nbeeb.main()\n")
    result = subprocess.run(
        [sys.executable, HEADLESS, program, "3"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("stage", ["stage3_screen", "stage4_screen"])
def test_stage_snapshots_draw_lines(stage):
    screen = load(P08 / "stages" / f"{stage}.py", stage)
    screen.mode(2)
    screen.gcol(0, 3)
    screen.move(0, 0)
    screen.draw(1279, 0)
    screen.vsync()
    assert screen._canvas.get_at_mapped((80, 255)) == 3
    assert screen._canvas.get_at_mapped((80, 200)) == 0


def test_stage4_adds_plot_and_point():
    screen = load(P08 / "stages" / "stage4_screen.py", "stage4_again")
    screen.mode(2)
    screen.move(200, 200)
    screen.move(1000, 200)
    screen.plot(85, 600, 800)
    assert screen.point(600, 400) == 7


def test_the_bug_hunt_file_really_has_the_bug():
    lines = load(P08 / "bughunt" / "lines.py", "buggy_lines")
    line, velocity, trail = [0.0, 0.0, 50.0, 50.0], [5.0, 5.0, 5.0, 5.0], []
    for _ in range(3):
        lines.step(line, velocity)
        lines.remember(trail, line, 1)
    assert trail[0][0] is trail[2][0], "every trail entry should be the same list"


SOLUTIONS_CHECK = """
import beeb

beeb.mode(2)
assert beeb.__file__.endswith("solutions/beeb/__init__.py"), beeb.__file__

# colour(): everything drawn in colour 1 turns blue at a stroke.
beeb.gcol(0, 1)
beeb.plot(69, 0, 0)
beeb.colour(1, 4)
assert beeb.screen._canvas.get_at((0, 255))[:3] == (0, 0, 255)

# Flashing: colour 9 is red for 25 frames, then cyan.
beeb.gcol(0, 9)
beeb.plot(69, 640, 512)
seen = set()
for _ in range(60):
    beeb.vsync()
    seen.add(tuple(beeb.screen._canvas.get_at((80, 127))[:3]))
assert seen == {(255, 0, 0), (0, 255, 255)}, seen

# circle() then fill(): the middle fills, the outside doesn't.
beeb.clg()
beeb.gcol(0, 2)
beeb.circle(640, 512, 200)
assert beeb.point(640, 512) == 0 and beeb.point(840, 512) == 2
beeb.fill(640, 512)
assert beeb.point(640, 512) == 2 and beeb.point(100, 100) == 0
beeb.fill(-50, -50)
"""


def test_solutions_package():
    result = subprocess.run(
        [sys.executable, "-c", SOLUTIONS_CHECK],
        cwd=P08 / "solutions",
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
