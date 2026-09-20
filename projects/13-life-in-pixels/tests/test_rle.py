import pytest
from life import PATTERNS
from life import parse as parse_picture

from pixel_life.rle import RLEError, parse

GLIDER = """
#N Glider
#C The smallest spaceship.
x = 3, y = 3, rule = B3/S23
bob$2bo$3o!
"""


def test_a_glider():
    assert parse(GLIDER) == parse_picture(PATTERNS["glider"])


def test_the_header_and_the_comments_are_optional():
    assert parse("bob$2bo$3o!") == parse(GLIDER)


def test_a_pattern_can_run_over_several_lines():
    assert parse("bob$\n2bo$\n3o!") == parse(GLIDER)


def test_blank_rows():
    assert parse("o3$o!") == {(0, 0), (0, 3)}


def test_the_gun_matches_the_one_drawn_by_hand():
    gun = """x = 36, y = 9, rule = B3/S23
    24bo11b$22bobo11b$12b2o6b2o12b2o$11bo3bo4b2o12b2o$2o8bo5bo3b2o14b$2o8b
    o3bob2o4bobo11b$10bo5bo7bo11b$11bo3bo20b$12b2o!"""
    assert parse(gun) == parse_picture(PATTERNS["gun"])


def test_anything_after_the_end_is_ignored():
    assert parse("o!ooo") == {(0, 0)}


@pytest.mark.parametrize(
    ("text", "complaint"),
    [("bob$2bo$3o", "no !"), ("", "no !"), ("bo?$o!", r"don't understand '\?'")],
)
def test_bad_patterns_are_reported(text, complaint):
    with pytest.raises(RLEError, match=complaint):
        parse(text)
