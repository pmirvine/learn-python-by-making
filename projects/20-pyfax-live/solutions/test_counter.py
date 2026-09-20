import sqlite3

from counter import SCHEMA, count_visit, most_visited


def test_counting_visits():
    db = sqlite3.connect(":memory:")
    db.execute(SCHEMA)
    assert [count_visit(db, 100), count_visit(db, 100), count_visit(db, 301)] == [
        1,
        2,
        1,
    ]
    assert count_visit(db, 100) == 3
    assert most_visited(db) == [(100, 3), (301, 1)]
