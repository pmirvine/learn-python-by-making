import random

import pytest

from main import ability_score, average, histogram, longest_streak, roll


def test_roll_gives_one_number_per_die():
    assert len(roll(5)) == 5
    assert len(roll()) == 2


def test_every_die_is_in_range():
    for _ in range(200):
        for die in roll(3, 20):
            assert 1 <= die <= 20


def test_the_same_seed_gives_the_same_rolls():
    random.seed(42)
    first = roll(10)
    random.seed(42)
    assert roll(10) == first


def test_ability_scores_run_from_3_to_18():
    scores = [ability_score() for _ in range(500)]
    assert min(scores) >= 3
    assert max(scores) <= 18


def test_histogram_scales_the_longest_bar_to_the_width():
    lines = histogram([2, 3, 3, 3, 3, 4, 4], width=8)
    assert lines == [
        "  2 ██ 14.3%",
        "  3 ████████ 57.1%",
        "  4 ████ 28.6%",
    ]


def test_histogram_shows_results_that_never_came_up():
    lines = histogram([1, 3])
    assert len(lines) == 3
    assert lines[1] == "  2  0.0%"


def test_average():
    assert average([1, 2, 3, 4]) == 2.5
    assert average([0.1, 0.2]) == pytest.approx(0.15)


def test_longest_streak():
    assert longest_streak([1, 2, 2, 3, 3, 3, 2]) == (3, 3)
    assert longest_streak([4, 4, 1, 1]) == (4, 2)
    assert longest_streak([6]) == (6, 1)


def test_longest_streak_of_nothing():
    assert longest_streak([]) == (None, 0)
