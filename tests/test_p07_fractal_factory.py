"""Repo-level checks for Project 7: stage snapshots, the type-in and the bug hunt.

The reader's own tests are in the project's tests/ folder.
"""

import importlib.util
from pathlib import Path

import pytest

pytest.importorskip("fractals", reason="needs the Project 7 environment")

P07 = "07-fractal-factory"
ROOT = Path(__file__).parent.parent / "projects" / P07


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_stage1_renders_in_greys():
    fields = load(ROOT / "stages" / "stage1_fields.py", "stage1_fields")
    render = load(ROOT / "stages" / "stage1_render.py", "stage1_render").render
    image = render(fields.mandelbrot, size=(12, 8), centre=-0.5 + 0j)
    assert image.mode == "L"
    assert image.getpixel((6, 4)) == 255
    assert 0.0 <= fields.plasma(1 + 1j) <= 1.0


def test_the_folklore_version_gives_the_same_answers():
    from fractals import mandelbrot

    squares = load(ROOT / "stages" / "stage4_squares_fields.py", "squares")
    for x in range(-20, 10):
        for y in range(-12, 13):
            point = complex(x / 10, y / 10)
            assert squares.mandelbrot(40)(point) == mandelbrot(40)(point)


def test_the_unoptimised_renderer_paints_the_same_picture():
    from fractals import PALETTES, mandelbrot, render

    slow = load(ROOT / "stages" / "stage3_render.py", "stage3_render").render
    options = {"size": (40, 30), "centre": -0.6 + 0j, "width": 3.6}
    before = slow(mandelbrot(30), PALETTES["fire"], **options)
    after = render(mandelbrot(30), PALETTES["fire"], **options)
    assert before.tobytes() == after.tobytes()


def test_the_ascii_mandelbrot(play):
    lines = play(f"{P07}/mandel.py", []).splitlines()
    assert len(lines) == 25
    assert all(len(line) == 79 for line in lines)
    assert lines[12].startswith("@@@@")
    assert lines[0] == lines[24]


def test_the_ruler_crashes_as_the_chapter_says(play, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(IndexError, match="out of range"):
        play(f"{P07}/bughunt/ruler.py", [])


def test_the_fixed_ruler(play, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    out = play(f"{P07}/solutions/bughunt/ruler.py", [])
    assert "A ruler from 0 to 1: fine." in out
    assert (tmp_path / "ruler.png").is_file()
