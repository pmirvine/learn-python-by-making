"""Repo-level checks for Project 13: the stage snapshot, the program, and a real git bisect.

The reader's own tests are in the project's tests/ folder.
"""

import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("pixel_life", reason="needs the Project 13 environment")
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

P13 = Path(__file__).parent.parent / "projects" / "13-life-in-pixels"
HEADLESS = Path(__file__).parent / "headless.py"


def test_the_first_view_and_the_faster_one_paint_the_same_picture():
    import pygame
    from life import soup
    from pixel_life.camera import Camera
    from pixel_life.simulation import Simulation
    from pixel_life.view import View

    spec = importlib.util.spec_from_file_location(
        "stage3_view", P13 / "stages" / "stage3_view.py"
    )
    stage3 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(stage3)

    pygame.init()
    simulation = Simulation(soup(200, 150, seed=4))
    camera = Camera(x=20.5, y=11.25, zoom=5)
    pictures = []
    for view_class in (stage3.View, View):
        window = pygame.display.set_mode((320, 240))
        view_class(window).draw(simulation, camera)
        pictures.append(pygame.image.tobytes(window, "RGB"))
    assert pictures[0] == pictures[1]


def test_the_program_runs(tmp_path):
    program = tmp_path / "play.py"
    program.write_text("from pixel_life.app import main\n\nmain()\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, HEADLESS, program, "20"],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stderr


@pytest.mark.skipif(shutil.which("git") is None, reason="needs git")
def test_bisecting_the_practice_history_finds_the_planted_commit(tmp_path):
    repo = tmp_path / "bisect-practice"
    subprocess.run(
        [sys.executable, P13 / "bughunt" / "make_history.py", repo], check=True
    )
    shutil.copy(P13 / "solutions" / "bughunt" / "test_cell_at.py", repo)

    def git(*arguments: str) -> str:
        done = subprocess.run(
            ["git", *arguments], cwd=repo, capture_output=True, text=True, check=True
        )
        return done.stdout

    assert len(git("log", "--oneline").splitlines()) == 14
    git("bisect", "start")
    git("bisect", "bad")
    git("bisect", "good", "v0.1")
    verdict = git(
        "bisect", "run", sys.executable, "-m", "pytest", "-q", "test_cell_at.py"
    )
    # Newer versions of Git say "the first 'bad' commit", with quotation marks.
    assert "8b17648" in verdict
    assert "is the first" in verdict
    assert "Simplify cell_at" in verdict


def test_the_type_in_unpacks_a_glider(play, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["unpack.py", "bob$2bo$3o!"])
    out = play("13-life-in-pixels/unpack.py", [])
    assert out.splitlines() == ["  ██  ", "    ██", "██████"]
