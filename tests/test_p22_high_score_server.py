"""Repo-level checks for Project 22: the bug hunt, the type-in, and the extras.

The reader's own tests are in the project's tests/ folder, and in snake-online's.
The live board was also watched in a real browser: see scripts/browser.py.
"""

import importlib.util
from pathlib import Path

import pytest

pytest.importorskip("high_scores", reason="needs the Project 22 environment")

from fastapi.testclient import TestClient

P22 = Path(__file__).parent.parent / "projects" / "22-high-score-server"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_bug_hunt_finds_nothing_though_the_scores_are_there(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    recent = load(P22 / "bughunt" / "recent.py", "recent")
    client = TestClient(recent.app)
    assert [row["player"] for row in client.get("/scores/snake").json()] == ["ADA"]
    assert client.get("/scores/recent").json() == []


def test_the_type_in_dice_api():
    dice = load(P22 / "dice.py", "dice")
    client = TestClient(dice.app)
    default = client.get("/roll").json()
    assert len(default["dice"]) == 2
    assert default["total"] == sum(default["dice"])
    many = client.get("/roll", params={"dice": 20, "sides": 2}).json()
    assert set(many["dice"]) <= {1, 2}
    assert client.get("/roll", params={"dice": 0}).status_code == 422
    assert client.get("/roll", params={"sides": "six"}).status_code == 422
    schema = client.get("/openapi.json").json()
    assert schema["paths"]["/roll"]["get"]["parameters"][0]["schema"]["maximum"] == 20


def test_main_makes_the_application_where_the_command_line_looks_for_it(
    tmp_path, monkeypatch
):
    monkeypatch.chdir(tmp_path)
    main = load(P22 / "main.py", "main")
    assert main.app.title == "High scores"
    assert (tmp_path / "scores.sqlite3").exists()


def test_the_page_needs_nothing_from_anybody_elses_server():
    static = P22 / "src" / "high_scores" / "static"
    for name in ("index.html", "board.js", "style.css"):
        assert "https://" not in (static / name).read_text(encoding="utf-8"), name
