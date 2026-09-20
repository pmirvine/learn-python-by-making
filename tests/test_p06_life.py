"""Repo-level checks for Project 6: stage snapshots, the type-in and the bug hunt.

The reader's own tests are in the project's tests/ folder.
"""

import importlib.util
import inspect
import sys
from pathlib import Path

import pytest

pytest.importorskip("life", reason="needs the Project 6 environment")

P06 = "06-life"
ROOT = Path(__file__).parent.parent / "projects" / P06

BLINKER = {(0, 1), (1, 1), (2, 1)}


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("stage", ["stage1_core", "stage2_core"])
def test_stage_cores_follow_the_rules(stage):
    core = load(ROOT / "stages" / f"{stage}.py", stage)
    assert len(list(core.neighbours((0, 0)))) == 8
    assert core.step(BLINKER) == {(1, 0), (1, 1), (1, 2)}
    assert core.step(core.step(BLINKER)) == BLINKER


def test_stage1_returns_a_list_and_stage2_a_generator():
    first = load(ROOT / "stages" / "stage1_core.py", "first")
    second = load(ROOT / "stages" / "stage2_core.py", "second")
    assert isinstance(first.neighbours((0, 0)), list)
    assert inspect.isgenerator(second.neighbours((0, 0)))
    assert next(second.generations(BLINKER)) == BLINKER


def test_stage2_animates_a_glider(monkeypatch, capsys):
    monkeypatch.setattr("time.sleep", lambda seconds: None)
    load(ROOT / "stages" / "stage2_cli.py", "stage2_cli").main()
    out = capsys.readouterr().out
    assert "Generation 99, population 5" in out


def test_rule_90_draws_a_triangle(play, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["rule.py"])
    lines = play(f"{P06}/rule.py", []).splitlines()
    assert len(lines) == 40
    assert lines[0].strip() == "█"
    assert lines[1].strip() == "█ █"
    assert lines[3].strip() == "█ █ █ █"


def test_rule_30_is_a_different_thing(play, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["rule.py", "30"])
    lines = play(f"{P06}/rule.py", []).splitlines()
    assert lines[1].strip() == "███"


def test_the_census_crashes_as_the_chapter_says(play):
    with pytest.raises(ValueError, match="empty"):
        play(f"{P06}/bughunt/census.py", [])


def test_the_fixed_census(play):
    out = play(f"{P06}/solutions/bughunt/census.py", [])
    assert out.rstrip().endswith("Peak population: 46")
