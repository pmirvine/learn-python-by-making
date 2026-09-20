"""The database: readers' letters, kept in SQLite."""

import sqlite3
from dataclasses import dataclass
from importlib.resources import files

from flask import current_app, g


@dataclass(frozen=True, slots=True)
class Letter:
    name: str
    message: str
    written: str


def get_db() -> sqlite3.Connection:
    """Return this request's connection to the database, opening it if need be."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(error: BaseException | None = None) -> None:
    """Close the connection, if this request ever opened one."""
    db: sqlite3.Connection | None = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    """Make the tables, if they aren't there already."""
    schema = (files("pyfax_live") / "schema.sql").read_text(encoding="utf-8")
    db = get_db()
    db.executescript(schema)


def add_letter(name: str, message: str) -> None:
    db = get_db()
    with db:
        db.execute("INSERT INTO letters (name, message) VALUES (?, ?)", (name, message))


def latest_letters(limit: int) -> list[Letter]:
    rows = get_db().execute(
        "SELECT name, message, written FROM letters ORDER BY id DESC LIMIT ?", (limit,)
    )
    return [Letter(row["name"], row["message"], row["written"]) for row in rows]
