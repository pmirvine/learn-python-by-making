import sqlite3

import pytest
from transcripts import KEEP, SCHEMA, add_lines, new_player, transcript


@pytest.fixture
def db() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.executescript(SCHEMA)
    return connection


def test_each_player_has_a_transcript_of_their_own(db):
    alice, bob = new_player(), new_player()
    assert alice != bob
    add_lines(db, alice, ["> south", "The Hall"])
    add_lines(db, bob, ["> dance", "I don't know how to dance."])
    add_lines(db, alice, ["> e"])
    assert transcript(db, alice) == ["> south", "The Hall", "> e"]
    assert transcript(db, bob) == ["> dance", "I don't know how to dance."]


def test_only_the_newest_lines_are_kept(db):
    player = new_player()
    add_lines(db, player, [f"line {n}" for n in range(KEEP + 50)])
    kept = transcript(db, player)
    assert len(kept) == KEEP
    assert kept[0] == "line 50"
    assert kept[-1] == f"line {KEEP + 49}"
