"""The failing tests that pin the chord's bug down. Try them on bughunt/chord.py."""

from array import array

from chord import chord, mix

from beeb.synth import LOUDEST


def test_loud_notes_can_be_mixed():
    loud = array("h", [30_000, -30_000, 30_000])
    mixed = mix(loud, loud, loud)
    assert len(mixed) == 3
    assert all(-LOUDEST <= sample <= LOUDEST for sample in mixed)


def test_a_loud_chord_can_be_made():
    data = chord([53, 69, 81], 0.1, volume=1.0)
    assert max(data) <= LOUDEST


def test_mixing_a_note_with_itself_changes_nothing():
    quiet = array("h", [100, -200, 300])
    assert mix(quiet, quiet) == quiet
