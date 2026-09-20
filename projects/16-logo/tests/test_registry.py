import inspect

import pytest

from logo.errors import LogoError
from logo.registry import COMMANDS, command, numeric, show


@pytest.fixture(autouse=True)
def leave_the_list_as_it_was():
    before = dict(COMMANDS)
    yield
    COMMANDS.clear()
    COMMANDS.update(before)


def test_command_lists_a_function_and_hands_it_back_unchanged():
    def hop(logo, distance, height):
        """HOP 10 5   Jump."""

    assert command("HOP", "HP")(hop) is hop
    assert COMMANDS["HP"] is COMMANDS["HOP"]
    assert COMMANDS["HOP"].inputs == 2
    assert COMMANDS["HOP"].name == "HOP"


def test_numeric_lets_numbers_through_and_stops_everything_else():
    @numeric
    def area(logo, width, height):
        return width * height

    assert area(None, 3, 4.5) == 13.5
    with pytest.raises(LogoError, match="AREA doesn't like TRUE as input"):
        area(None, 3, True)


def test_a_wrapped_function_still_looks_like_itself():
    @numeric
    def hop(logo, distance, height):
        """HOP 10 5   Jump."""

    assert hop.__name__ == "hop"
    assert hop.__doc__ == "HOP 10 5   Jump."
    assert list(inspect.signature(hop).parameters) == ["logo", "distance", "height"]


def test_which_is_why_the_order_of_the_decorators_works():
    @command("HOP")
    @numeric
    def hop(logo, distance, height):
        """HOP 10 5   Jump."""

    assert COMMANDS["HOP"].inputs == 2
    with pytest.raises(LogoError, match="HOP doesn't like"):
        COMMANDS["HOP"].function(None, "high", 5)


def test_every_command_says_how_to_use_it():
    for name, primitive in COMMANDS.items():
        assert (primitive.function.__doc__ or "").startswith(primitive.name), name


def test_show():
    assert show(3.0) == "3"
    assert show(2.5) == "2.5"
    assert show(False) == "FALSE"
    assert show("WORD") == "WORD"
