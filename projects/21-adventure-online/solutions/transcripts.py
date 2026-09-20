"""Extend 2: keep each player's transcript on the server, since a cookie is too small.

The cookie holds one short random id. Everything else is in SQLite, under that id.
"""

import secrets
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS lines (
    id INTEGER PRIMARY KEY,
    player TEXT NOT NULL,
    line TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS lines_by_player ON lines (player, id);
"""
KEEP = 200


def new_player() -> str:
    """Return an id that nobody could guess, to go in a new player's cookie."""
    return secrets.token_urlsafe(16)


def add_lines(db: sqlite3.Connection, player: str, lines: list[str]) -> None:
    """Add to a player's transcript, and throw away all but the newest 200 lines."""
    with db:
        db.executemany(
            "INSERT INTO lines (player, line) VALUES (?, ?)",
            [(player, line) for line in lines],
        )
        db.execute(
            """
            DELETE FROM lines WHERE player = ? AND id NOT IN (
                SELECT id FROM lines WHERE player = ? ORDER BY id DESC LIMIT ?
            )
            """,
            (player, player, KEEP),
        )


def transcript(db: sqlite3.Connection, player: str) -> list[str]:
    rows = db.execute("SELECT line FROM lines WHERE player = ? ORDER BY id", (player,))
    return [line for (line,) in rows]
