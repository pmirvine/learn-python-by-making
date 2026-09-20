from itertools import islice

import pytest

from life import (
    PATTERNS,
    generations,
    neighbours,
    normalise,
    parse,
    period,
    shift,
    step,
)


def test_a_cell_has_eight_neighbours_and_is_not_one_of_them():
    around = set(neighbours((5, 5)))
    assert len(around) == 8
    assert (5, 5) not in around
    assert {(4, 4), (6, 6), (5, 4)} <= around


def test_an_empty_universe_stays_empty():
    assert step(set()) == set()


def test_a_lonely_cell_dies():
    assert step({(0, 0)}) == set()


def test_three_neighbours_make_a_birth():
    corner = {(0, 0), (1, 0), (0, 1)}
    assert (1, 1) in step(corner)


def test_step_leaves_its_argument_alone():
    blinker = parse(PATTERNS["blinker"])
    before = blinker.copy()
    step(blinker)
    assert blinker == before


def test_a_blinker_blinks():
    across = {(0, 1), (1, 1), (2, 1)}
    down = {(1, 0), (1, 1), (1, 2)}
    assert step(across) == down
    assert step(down) == across


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("block", 1),
        ("beehive", 1),
        ("blinker", 2),
        ("toad", 2),
        ("glider", 4),
        ("lwss", 4),
    ],
)
def test_periods(name, expected):
    assert period(parse(PATTERNS[name])) == expected


def test_a_pattern_that_dies_out_has_period_zero():
    assert period({(0, 0), (1, 0)}) == 0


def test_period_gives_up_at_the_limit():
    assert period(parse(PATTERNS["acorn"]), limit=50) is None


def test_a_glider_moves_one_cell_diagonally_every_four_generations():
    glider = parse(PATTERNS["glider"])
    later = next(islice(generations(glider), 4, None))
    assert later == shift(glider, 1, 1)


def test_the_gun_fires_a_five_cell_glider_every_thirty_generations():
    gun = parse(PATTERNS["gun"])
    populations = [len(universe) for universe in islice(generations(gun), 0, 121, 30)]
    assert populations == [36, 41, 46, 51, 56]
    assert period(gun, limit=100) is None


def test_generations_starts_with_the_universe_it_was_given():
    toad = parse(PATTERNS["toad"])
    first, second, third = islice(generations(toad), 3)
    assert first == toad
    assert second != toad
    assert third == toad


def test_normalise_ignores_position():
    glider = parse(PATTERNS["glider"])
    assert normalise(shift(glider, 40, -7)) == normalise(glider)
    assert normalise(set()) == frozenset()
