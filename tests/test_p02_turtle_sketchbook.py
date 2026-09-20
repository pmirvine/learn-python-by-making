"""Project 2 comes before the tutorial teaches testing, so its tests live here.

Every program is run twice: on paper (see paperturtle.py), which works on any
machine, and against the real turtle module wherever there's a display.
"""

import random
import runpy
import subprocess
import sys
from pathlib import Path

import paperturtle
import pytest

P02 = Path(__file__).parent.parent / "projects" / "02-turtle-sketchbook"
RUNNER = Path(__file__).parent / "turtle_runner.py"

BRANCHES = 2**8 - 1  # a tree of depth 8 has one branch, then 2, then 4...
PROGRAMS = {
    "stages/stage1_square.py": 4,
    "spiral.py": 100,
    "stages/stage2.py": 36 * 6,
    "stages/stage3.py": 60 * 5 + 18 * 6,
    "main.py": 60 * 5 + 18 * 6 + 3 * BRANCHES,
    "koch.py": 3 * 4**4,
    "solutions/filled.py": None,
    "solutions/seasons.py": None,
    "solutions/redraw.py": None,
}


@pytest.fixture
def paper(monkeypatch):
    """Swap the real turtle module for the paper one, with a clean sheet."""
    monkeypatch.setitem(sys.modules, "turtle", paperturtle)
    paperturtle.reset()
    random.seed(2)
    return paperturtle


@pytest.mark.parametrize(("script", "lines"), PROGRAMS.items())
def test_on_paper(paper, script, lines):
    runpy.run_path(str(P02 / script), run_name="__main__")
    if lines is None:
        assert paper.drawn("line")
    else:
        assert len(paper.drawn("line")) == lines


def test_polygon_and_tree_leave_the_pen_as_they_found_it(paper):
    sketchbook = runpy.run_path(str(P02 / "main.py"))
    pen = paper.Turtle()
    pen.goto(30, -40)
    pen.setheading(90)

    sketchbook["polygon"](pen, 7, 50)
    sketchbook["tree"](pen, 60, 6)

    assert pen.position() == pytest.approx((30, -40))
    assert pen.heading() == pytest.approx(90)


def test_stars_choose_their_own_sizes(paper):
    sketchbook = runpy.run_path(str(P02 / "main.py"))
    pen = paper.Turtle()
    for _ in range(10):
        sketchbook["star"](pen, (0, 0))
    lengths = {round(pen.distance(start)) for _, start, *_ in paper.drawn("line")}
    assert len(lengths) > 3, "every star came out the same size"


def test_redraw_binds_a_key_that_draws_again(paper):
    runpy.run_path(str(P02 / "solutions" / "redraw.py"), run_name="__main__")
    first = len(paper.drawn("line"))
    paper.press("space")
    assert len(paper.drawn("line")) == first, "the old picture should be cleared"


def has_display() -> bool:
    check = "import tkinter; tkinter.Tk().destroy()"
    result = subprocess.run(
        [sys.executable, "-c", check], capture_output=True, timeout=60, check=False
    )
    return result.returncode == 0


@pytest.mark.skipif(not has_display(), reason="the real turtle needs a display")
@pytest.mark.parametrize("script", PROGRAMS)
def test_with_the_real_turtle(script):
    result = subprocess.run(
        [sys.executable, RUNNER, P02 / script],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stderr
