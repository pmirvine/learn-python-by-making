"""The failing test, for the colleague's parser. It passes with yours."""

from tiny_basic.nodes import Binary, Number
from tiny_basic.parser import Parser


def test_taking_away_goes_from_left_to_right():
    assert Parser("10 - 4 - 3").expression() == Binary(
        Binary(Number(10), "-", Number(4)), "-", Number(3)
    )


def test_so_does_dividing():
    assert Parser("100 / 10 / 5").expression() == Binary(
        Binary(Number(100), "/", Number(10)), "/", Number(5)
    )


def test_but_powers_still_go_from_right_to_left():
    assert Parser("2 ^ 3 ^ 2").expression() == Binary(
        Number(2), "^", Binary(Number(3), "^", Number(2))
    )
