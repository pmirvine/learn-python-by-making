"""Repo-level checks for the Pyxel side quest.

Pyxel can't open a window where there's no display, and so the game is run
against a stand-in, tests/fakepyxel.py. The real thing has been run by hand, and
by scripts/screenshots_p15x.py, which made the picture in the chapter.
"""

import runpy
import sys
from pathlib import Path

import fakepyxel
import pytest

QUEST = Path(__file__).parent.parent / "projects" / "15x-pyxel-side-quest"


def play(monkeypatch, frames: int, keys=lambda frame: set()) -> dict:
    fakepyxel.reset(frames, keys)
    monkeypatch.setitem(sys.modules, "pyxel", fakepyxel)
    return runpy.run_path(str(QUEST / "meteors.py"))


def test_the_stand_in_has_nothing_that_the_real_pyxel_lacks():
    # On Linux, Pyxel needs the system's SDL2, and a machine may well not have it.
    real_pyxel = pytest.importorskip(
        "pyxel", reason="needs Pyxel, and SDL2 to go with it", exc_type=ImportError
    )
    ours = [
        name
        for name, value in vars(fakepyxel).items()
        if name.isupper() or (callable(value) and value.__module__ == "fakepyxel")
    ]
    ours = [name for name in ours if name not in ("Image", "Sound", "reset", "held")]
    assert len(ours) >= 12
    for name in ours:
        assert hasattr(real_pyxel, name), name
    assert hasattr(real_pyxel.Image, "set")
    assert hasattr(real_pyxel.Sound, "set")


def test_the_sprite_from_project_15_is_loaded_in_pyxel_colours(monkeypatch):
    play(monkeypatch, 1)
    rows = fakepyxel.images[0].rows
    assert len(rows) == 16
    assert rows[0] == "fffffff77fffffff"
    assert rows[8] == "ffff87777778ffff"
    assert fakepyxel.sounds[0].settings[0] == "c3g3"


def test_a_frame_has_a_sky_some_stars_a_ship_and_a_score(monkeypatch):
    play(monkeypatch, 30)
    kinds = [call[0] for call in fakepyxel.frames[-1]]
    assert kinds[0] == "cls"
    assert kinds.count("pset") == 30
    assert kinds.count("blt") == 1
    assert ("text", 4, 4, "SCORE 0", 7) in fakepyxel.frames[-1]
    assert kinds.count("circ") == 2 * 4  # a meteor every 8 frames, two circles each


def ship_x(frame: list[tuple]) -> float:
    return next(call[1] for call in frame if call[0] == "blt")


def test_holding_a_key_moves_the_ship_and_the_edge_stops_it(monkeypatch):
    play(monkeypatch, 40, keys=lambda frame: {fakepyxel.KEY_RIGHT})
    assert ship_x(fakepyxel.frames[0]) == 58
    assert ship_x(fakepyxel.frames[1]) == 60
    assert ship_x(fakepyxel.frames[-1]) == 128 - 16


def test_sooner_or_later_a_ship_that_stays_put_is_hit(monkeypatch):
    play(monkeypatch, 3000)
    assert (0, 1) in fakepyxel.played
    last = fakepyxel.frames[-1]
    assert last[0] == ("cls", 2)
    assert any(call[0] == "text" and call[3] == "SPACE TO RETRY" for call in last)


def test_space_starts_again(monkeypatch):
    play(monkeypatch, 3000, keys=lambda frame: {fakepyxel.KEY_SPACE} & {frame % 2 * 3})
    crashes = fakepyxel.played.count((0, 1))
    assert crashes > 1
