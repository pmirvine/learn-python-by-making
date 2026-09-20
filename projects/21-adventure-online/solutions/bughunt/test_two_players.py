"""The failing test for the colleague's game: two players, who ought not to meet."""

import importlib.util
from pathlib import Path

from flask import Flask

from cupboard_web import create_app


def colleagues_app() -> Flask:
    path = Path(__file__).parent.parent.parent / "bughunt" / "shared.py"
    spec = importlib.util.spec_from_file_location("shared", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.app


def test_in_the_colleagues_game_everybody_is_the_same_player():
    app = colleagues_app()
    alice, bob = app.test_client(), app.test_client()
    alice.post("/command", data={"text": "south"})
    assert "Moves: 1" in bob.get("/").text
    assert "The Hall" in bob.get("/").text


def test_in_yours_they_are_not():
    app = create_app({"TESTING": True, "SECRET_KEY": "only for tests"})
    alice, bob = app.test_client(), app.test_client()
    page = alice.get("/").text
    token = page.split('name="token" value="')[1].split('"')[0]
    alice.post("/command", data={"text": "south", "token": token})
    assert "Moves: 1" in alice.get("/").text
    assert "Moves: 0" in bob.get("/").text
