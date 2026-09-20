import pytest
from duel import wins
from yahtzee import best_group


def test_best_group():
    assert best_group([1, 2, 3, 4, 5]) == 1
    assert best_group([6, 2, 6, 2, 6]) == 3
    assert best_group([4, 4, 4, 4, 4]) == 5


def test_wins_counts_each_round_once():
    assert wins([5, 3, 9], [4, 3, 12]) == (1, 1, 1)


def test_wins_insists_on_equal_numbers_of_rounds():
    with pytest.raises(ValueError, match="shorter"):
        wins([1, 2, 3], [1, 2])
