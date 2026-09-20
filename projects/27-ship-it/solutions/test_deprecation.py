"""Extend 1: changing your mind, politely. A renamed function that still works, and says so."""

import warnings

import pytest


def block(left: int, bottom: int, right: int, top: int) -> tuple[int, int, int, int]:
    return left, bottom, right, top


@warnings.deprecated("rectangle() is now block(), and will go in 2.0.")
def rectangle(
    left: int, bottom: int, right: int, top: int
) -> tuple[int, int, int, int]:
    return block(left, bottom, right, top)


def test_the_old_name_still_works_and_says_that_it_is_going():
    with pytest.warns(DeprecationWarning, match=r"now block\(\)"):
        assert rectangle(0, 0, 10, 10) == (0, 0, 10, 10)


def test_the_new_name_is_quiet():
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert block(0, 0, 10, 10) == (0, 0, 10, 10)
