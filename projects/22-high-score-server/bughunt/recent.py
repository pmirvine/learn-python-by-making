"""A colleague has added an address for the latest scores, from any game.

    uv run fastapi dev bughunt/recent.py

Then go to http://127.0.0.1:8000/scores/recent. "It doesn't crash," they say.
"It just never finds anything. But the scores are there: look at /scores/snake."
"""

from contextlib import closing
from pathlib import Path

from fastapi import FastAPI

from high_scores import create_app, store
from high_scores.app import Db
from high_scores.models import NewScore, Score

DATABASE = Path("bughunt-scores.sqlite3")


def make_app(database: Path = DATABASE) -> FastAPI:
    app = create_app(database)

    @app.get("/scores/recent")
    def recent_scores(db: Db) -> list[Score]:
        """The five latest scores, from every game."""
        rows = db.execute(f"{store.RANKED} ORDER BY id DESC LIMIT 5")
        return [Score(**row) for row in rows]

    return app


def add_some_scores(database: Path) -> None:
    with closing(store.connect(database)) as db:
        if not store.games(db):
            for game, player, score in [
                ("snake", "ADA", 120),
                ("breakout", "BOB", 900),
            ]:
                store.add(db, NewScore(game=game, player=player, score=score))


app = make_app()
add_some_scores(DATABASE)
