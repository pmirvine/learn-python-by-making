"""The failing test for the colleague's address, and a version that passes it."""

import importlib.util
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from high_scores import create_app, store
from high_scores.app import Db, router
from high_scores.models import Score


def colleagues_app(database: Path) -> FastAPI:
    path = Path(__file__).parent.parent.parent / "bughunt" / "recent.py"
    spec = importlib.util.spec_from_file_location("recent", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.DATABASE.unlink(missing_ok=True)
    return module.make_app(database)


def mended_app(database: Path) -> FastAPI:
    """The same address, put on the list BEFORE the one with {game} in it."""
    app = FastAPI()
    app.state.database = database

    @app.get("/scores/recent")
    def recent_scores(db: Db) -> list[Score]:
        rows = db.execute(f"{store.RANKED} ORDER BY id DESC LIMIT 5")
        return [Score(**row) for row in rows]

    app.include_router(router)
    return app


def play(client: TestClient) -> None:
    for game, player, score in [("snake", "ADA", 120), ("breakout", "BOB", 900)]:
        body = {"game": game, "player": player, "score": score}
        assert client.post("/scores", json=body).status_code == 201


def test_the_colleagues_address_is_taken_for_a_game_called_recent(tmp_path):
    client = TestClient(colleagues_app(tmp_path / "scores.sqlite3"))
    play(client)
    assert client.get("/scores/recent").json() == []


def test_the_mended_one_finds_the_latest_scores(tmp_path):
    create_app(tmp_path / "scores.sqlite3")
    client = TestClient(mended_app(tmp_path / "scores.sqlite3"))
    play(client)
    latest = client.get("/scores/recent").json()
    assert [row["player"] for row in latest] == ["BOB", "ADA"]
