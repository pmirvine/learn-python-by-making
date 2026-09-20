"""Repo-level checks for Project 5: the programs a reader runs, end to end.

The reader's own tests are in the project's tests/ folder.
"""

import importlib.util
from pathlib import Path

import pytest

P05 = "05-colossal-cupboard"
ROOT = Path(__file__).parent.parent / "projects" / P05

pytest.importorskip("cupboard", reason="needs the Project 5 environment")


def run_main(module_file: Path, monkeypatch, capsys, replies, name="stage"):
    """Load a file as a module and call its main(), with scripted input."""
    answers = iter(replies)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))
    spec = importlib.util.spec_from_file_location(name, module_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.main()
    return capsys.readouterr().out


def test_stage1_walks_about(monkeypatch, capsys):
    out = run_main(
        ROOT / "stages" / "stage1_init.py",
        monkeypatch,
        capsys,
        ["s", "xyzzy", "n", "n", "q"],
    )
    assert out.count("The Cupboard Under the Stairs") == 3
    assert "The Hall" in out
    assert out.count("You can't go that way.") == 2


def test_stage2_plays_the_game(monkeypatch, capsys):
    out = run_main(
        ROOT / "stages" / "stage2_init.py",
        monkeypatch,
        capsys,
        ["s", "e", "take torch", "i", "quit"],
    )
    assert "You're carrying: torch." in out
    assert out.rstrip().endswith("Bye.")


def test_the_finished_game_saves_and_restores(monkeypatch, capsys, tmp_path):
    monkeypatch.chdir(tmp_path)
    replies = [
        "restore",
        "s",
        "e",
        "take torch",
        "save",
        "drop torch",
        "restore",
        "i",
        "quit",
    ]
    out = run_main(
        ROOT / "src" / "cupboard" / "__init__.py", monkeypatch, capsys, replies, "game"
    )
    assert "There's no saved game to restore." in out
    assert "Saved." in out
    assert "Restored." in out
    assert "You're carrying: torch." in out
    assert (tmp_path / "cupboard-save.json").is_file()


def test_langtons_ant_builds_a_highway(play):
    out = play(f"{P05}/ant.py", [])
    lines = out.splitlines()
    assert len(lines) > 40
    assert all(set(line) <= {"█", " "} for line in lines)


def test_the_pantry_shows_its_symptom(play):
    out = play(f"{P05}/bughunt/pantry.py", ["take jam", "take marmalade", "q"])
    assert "I can't see any jam here." in out
    assert "Taken." in out


def test_the_fixed_pantry(play):
    out = play(f"{P05}/solutions/bughunt/pantry.py", ["take jam", "q"])
    assert "Taken." in out
