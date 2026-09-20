"""Extend 1: count the visits to each page, in the database.

`INSERT ... ON CONFLICT ... DO UPDATE` is an "upsert": make the row if it isn't
there, and change it if it is, in one statement, which nobody can get between.
"""

import sqlite3

SCHEMA = "CREATE TABLE IF NOT EXISTS visits (page INTEGER PRIMARY KEY, count INTEGER NOT NULL)"
UPSERT = """
    INSERT INTO visits (page, count) VALUES (?, 1)
    ON CONFLICT (page) DO UPDATE SET count = count + 1
    RETURNING count
"""


def count_visit(db: sqlite3.Connection, page: int) -> int:
    """Note one more visit to a page, and return how many that makes."""
    with db:
        (count,) = db.execute(UPSERT, (page,)).fetchone()
    return count


def most_visited(db: sqlite3.Connection, limit: int = 5) -> list[tuple[int, int]]:
    rows = db.execute(
        "SELECT page, count FROM visits ORDER BY count DESC, page LIMIT ?", (limit,)
    )
    return [(page, count) for page, count in rows]
