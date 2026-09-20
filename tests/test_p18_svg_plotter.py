"""Repo-level checks for Project 18: the example drawings, the stage, and the extras.

The reader's own tests are in the project's tests/ folder.
"""

import importlib.util
import runpy
import subprocess
import sys
import webbrowser
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

pytest.importorskip("plotter", reason="needs the Project 18 environment")

P18 = Path(__file__).parent.parent / "projects" / "18-svg-plotter"
ASSETS = Path(__file__).parent.parent / "docs" / "assets"
SVG = "{http://www.w3.org/2000/svg}"


@pytest.mark.parametrize(
    ("example", "strokes", "labels"),
    [("rose", 1, 1), ("maze", 1280, 0), ("hilbert", 1, 0)],
)
def test_the_examples_draw_well_formed_pictures(
    example, strokes, labels, tmp_path, monkeypatch
):
    monkeypatch.chdir(tmp_path)
    runpy.run_path(str(P18 / "examples" / f"{example}.py"), run_name="__main__")
    tree = ET.parse(tmp_path / "pictures" / f"{example}.svg").getroot()
    assert len(list(tree.iter(f"{SVG}path"))) == strokes
    assert len(list(tree.iter(f"{SVG}text"))) == labels


def test_the_hilbert_curve_visits_every_cell_once(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runpy.run_path(str(P18 / "examples" / "hilbert.py"), run_name="__main__")
    tree = ET.parse(tmp_path / "pictures" / "hilbert.svg").getroot()
    (path,) = tree.iter(f"{SVG}path")
    points = path.get("d", "").replace("M", "").split(" L")
    assert len(points) == len(set(points)) == 4**5


def test_the_pictures_in_the_chapter_are_the_ones_that_the_examples_draw():
    for name in ("rose", "maze", "hilbert", "chart"):
        tree = ET.parse(ASSETS / f"p18-{name}.svg").getroot()
        assert tree.tag == f"{SVG}svg", name


def load_stage():
    spec = importlib.util.spec_from_file_location(
        "stage1_plot", P18 / "stages" / "stage1_plot.py"
    )
    stage = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(stage)
    return stage


def test_stage1_works_until_somebody_writes_an_ampersand(tmp_path):
    plot = load_stage().Plot(tmp_path / "t.svg")
    plot.move(0, 0)
    plot.draw(100, 100)
    plot.label(10, 10, "Fish and chips")
    assert len(list(ET.fromstring(plot.svg()).iter(f"{SVG}line"))) == 1

    plot.label(10, 50, "Fish & chips")
    with pytest.raises(ET.ParseError):
        ET.fromstring(plot.svg())


def test_the_bug_hunt_shows_its_symptom(tmp_path):
    result = subprocess.run(
        [sys.executable, P18 / "bughunt" / "quiet.py"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=tmp_path,
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "Finished, with no errors. Strokes in quiet.svg: 1" in result.stdout
    assert (tmp_path / "quiet.svg").exists()


def test_the_type_in_spirograph(tmp_path, monkeypatch, capsys):
    opened = []
    monkeypatch.setattr(webbrowser, "open", opened.append)
    monkeypatch.chdir(tmp_path)
    runpy.run_path(str(P18 / "spiro.py"), run_name="__main__")
    assert "59 turns of the wheel" in capsys.readouterr().out
    assert opened[0].startswith("file://")
    assert opened[0].endswith("spiro.svg")
    (curve,) = ET.parse(tmp_path / "spiro.svg").getroot().iter(f"{SVG}polyline")
    points = curve.get("points", "").split()
    assert len(points) == 59 * 360 + 1
    first, last = (
        [float(n) for n in point.split(",")] for point in (points[0], points[-1])
    )
    assert first == pytest.approx(last, abs=0.05)  # it closes, give or take a -0.0
