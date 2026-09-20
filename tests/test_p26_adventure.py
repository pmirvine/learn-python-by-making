"""Project 26: the bug hunt, the type-in listing and the road not taken."""

import runpy
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT = Path(__file__).parent.parent / "projects" / "26-adventure-third-edition"


def run(*args: str) -> str:
    done = subprocess.run(
        ["uv", "run", "--project", str(PROJECT), *args],
        capture_output=True, text=True, encoding="utf-8", cwd=PROJECT, check=True, timeout=120,
    )  # fmt: skip
    return done.stdout


def test_the_bug_hunt_really_does_forget_to_forget():
    out = run("python", "bughunt/take_all.py")
    assert "Taken: torch." in out
    assert "Taken back." in out
    assert out.strip().endswith("Carrying: torch")
    assert "You can see: torch." not in out.split("(F4)")[1]


def test_the_type_in_listing_fits_the_page():
    lines = (PROJECT / "lift.py").read_text(encoding="utf-8").splitlines()
    assert len(lines) <= 30


def test_the_type_in_listing_is_a_game_and_the_app_will_play_it():
    code = """
import asyncio, runpy
from textual.widgets import Input
from adventure.app import AdventureApp, TheEnd
from adventure.widgets import MapPanel

started = []
AdventureApp.run = lambda self, **_: started.append(self)
runpy.run_path("lift.py")
(app,) = started

async def ride():
    async with app.run_test() as pilot:
        for command in ["down", "up", "up", "up"]:
            app.query_one(Input).value = command
            await pilot.press("enter")
        lines = [line.text for line in app.query_one("#transcript").lines]
        assert "The lift doesn't budge." in lines, lines
        assert "Ding! The doors open on Toys." in lines, lines
        assert not app.query(MapPanel)
        assert app.check_action("undo", ()) is False
        assert isinstance(app.screen, TheEnd)
        print("rode to", app.game.status()["Floor"])

asyncio.run(ride())
"""
    assert run("python", "-c", code).strip() == "rode to the roof garden"


def test_the_abstract_version_complains_when_an_object_is_made():
    sys.path.insert(0, str(PROJECT / "stages"))
    try:
        abc_game = runpy.run_path(str(PROJECT / "stages" / "game_abc.py"))
    finally:
        sys.path.pop(0)
    base = abc_game["Game"]

    class Half(base):
        def opening(self) -> str:
            return "Hello"

    with pytest.raises(TypeError, match="abstract"):
        Half()

    class Whole(Half):
        over = False

        def play(self, text: str) -> str:
            return text.upper()

    assert Whole().play_all(["a", "b"]) == ["A", "B"]
    assert Whole().status() == {}
