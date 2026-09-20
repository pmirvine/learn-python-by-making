"""Keeping the scores, in SQLite. Nothing in here knows about the web."""

import sqlite3
from pathlib import Path

from high_scores.models import GameSummary, NewScore, Score

SCHEMA = """
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY,
    game TEXT NOT NULL,
    player TEXT NOT NULL,
    score INTEGER NOT NULL,
    "when" TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS scores_by_game ON scores (game, score DESC);
"""
RANKED = """
    SELECT id, game, player, score, "when",
           (SELECT COUNT(*) + 1 FROM scores AS better
             WHERE better.game = scores.game AND better.score > scores.score) AS rank
      FROM scores
"""


def connect(database: Path) -> sqlite3.Connection:
    # FastAPI may open a connection in one thread and use it in another. That's
    # safe here, since a connection belongs to one request, and SQLite needs telling.
    db = sqlite3.connect(database, check_same_thread=False)
    db.row_factory = sqlite3.Row
    return db


def init(db: sqlite3.Connection) -> None:
    db.executescript(SCHEMA)


def add(db: sqlite3.Connection, new: NewScore) -> Score:
    with db:
        cursor = db.execute(
            "INSERT INTO scores (game, player, score) VALUES (?, ?, ?)",
            (new.game, new.player, new.score),
        )
    row = db.execute(f"{RANKED} WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return Score(**row)


def top(db: sqlite3.Connection, game: str, limit: int) -> list[Score]:
    rows = db.execute(
        f"{RANKED} WHERE game = ? ORDER BY score DESC, id LIMIT ?", (game, limit)
    )
    return [Score(**row) for row in rows]


def games(db: sqlite3.Connection) -> list[GameSummary]:
    rows = db.execute(
        "SELECT game, COUNT(*) AS plays, MAX(score) AS best FROM scores "
        "GROUP BY game ORDER BY game"
    )
    return [GameSummary(**row) for row in rows]


def newest(db: sqlite3.Connection, game: str) -> int:
    """Return the id of the latest score for a game, or 0 if there aren't any."""
    (found,) = db.execute(
        "SELECT COALESCE(MAX(id), 0) FROM scores WHERE game = ?", (game,)
    ).fetchone()
    return found
