"""A colleague has added a way of finding one reader's letters. Mr O'Brien can't use it.

uv run bughunt/search.py
"""

import sqlite3

LETTERS = [
    ("Enid", "More hedgehogs, please."),
    ("O'Brien", "Can the turtle do our car park next?"),
    ("Enid", "I demand a recount."),
    ("Editor", "NOT FOR PUBLICATION: the hedgehog's agent wants paying."),
]


def letters_from(db: sqlite3.Connection, name: str) -> list[str]:
    """Return the letters that somebody has written."""
    query = f"SELECT message FROM letters WHERE name = '{name}'"
    return [row[0] for row in db.execute(query)]


def main() -> None:
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE letters (name TEXT, message TEXT)")
    db.executemany("INSERT INTO letters VALUES (?, ?)", LETTERS)

    for name in ("Enid", "Nobody", "O'Brien"):
        print(f"Letters from {name}:")
        for message in letters_from(db, name):
            print("   ", message)


if __name__ == "__main__":
    main()
