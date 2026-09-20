"""The failing tests for the colleague's search, and the mended search that passes them."""

import sqlite3

import pytest

LETTERS = [
    ("Enid", "More hedgehogs, please."),
    ("O'Brien", "Can the turtle do our car park next?"),
    ("Editor", "NOT FOR PUBLICATION"),
]


def letters_from(db: sqlite3.Connection, name: str) -> list[str]:
    """Return the letters that somebody has written. The name travels separately."""
    rows = db.execute("SELECT message FROM letters WHERE name = ?", (name,))
    return [row[0] for row in rows]


@pytest.fixture
def db() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.execute("CREATE TABLE letters (name TEXT, message TEXT)")
    connection.executemany("INSERT INTO letters VALUES (?, ?)", LETTERS)
    return connection


def test_a_name_with_an_apostrophe_in_it(db):
    assert letters_from(db, "O'Brien") == ["Can the turtle do our car park next?"]


def test_a_name_that_is_really_a_piece_of_sql_finds_nothing(db):
    assert letters_from(db, "' OR '1'='1") == []
