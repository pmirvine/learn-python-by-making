import pytest
from life import PATTERNS, normalise, parse
from rle_writer import to_rle

from pixel_life import rle


def test_a_glider():
    # The dead cell at the end of the first row is left out: it goes without saying.
    assert (
        to_rle(parse(PATTERNS["glider"])) == "x = 3, y = 3, rule = B3/S23\nbo$2bo$3o!\n"
    )


@pytest.mark.parametrize("name", PATTERNS)
def test_every_pattern_survives_the_round_trip(name):
    cells = parse(PATTERNS[name])
    assert rle.parse(to_rle(cells)) == cells


def test_position_is_not_recorded():
    far_away = {(100, -50), (101, -50), (100, -48)}
    assert normalise(rle.parse(to_rle(far_away))) == normalise(far_away)


def test_nothing_at_all():
    assert rle.parse(to_rle(set())) == set()
