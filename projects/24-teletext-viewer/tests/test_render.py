import unicodedata

import pytest
from pyfax import Colour, Page
from rich.color import Color

from teleview.glyphs import GLYPHS, braille, quadrant, sextant
from teleview.render import page_text


@pytest.mark.parametrize("dots", range(64))
def test_every_sextant_is_the_one_that_its_name_says(dots):
    """Unicode calls them BLOCK SEXTANT-135, and so on, after the squares that are lit."""
    lit = "".join(str(square + 1) for square in range(6) if dots >> square & 1)
    expected = {
        "": "SPACE",
        "135": "LEFT HALF BLOCK",
        "246": "RIGHT HALF BLOCK",
        "123456": "FULL BLOCK",
    }.get(lit, f"BLOCK SEXTANT-{lit}")
    assert unicodedata.name(sextant(dots)) == expected


def test_there_is_a_different_braille_pattern_for_each_too():
    patterns = {braille(dots) for dots in range(64)}
    assert len(patterns) == 64
    assert braille(0) == "⠀"
    assert braille(63) == "⣿"


@pytest.mark.parametrize(
    ("dots", "character"),
    [
        (0b000000, " "),
        (0b000001, "▘"),
        (0b000011, "▀"),
        (0b010101, "▌"),
        (0b010000, "▖"),
        (0b000100, "▖"),
        (0b111100, "▄"),
        (0b100001, "▚"),
        (0b111111, "█"),
    ],
)
def test_quadrants_are_the_nearest_that_four_squares_can_come(dots, character):
    assert quadrant(dots) == character


def test_the_ways_of_drawing_have_names():
    assert sorted(GLYPHS) == ["braille", "quadrant", "sextant"]
    assert all(len(glyph(n)) == 1 for glyph in GLYPHS.values() for n in range(64))


def test_a_page_becomes_24_lines_of_40_characters_without_its_own_top_line():
    page = Page(100, "Test")
    page.write(0, 0, "P100", Colour.YELLOW)
    page.write(1, 0, "HEADLINE", Colour.YELLOW)
    page.picture(2, 0, ["##", "#.", "##"], Colour.RED)
    lines = page_text(page).plain.split("\n")
    assert len(lines) == 24
    assert {len(line) for line in lines} == {40}
    assert lines[0].startswith("HEADLINE")
    assert lines[1][0] == sextant(0b110111)
    assert page_text(page, braille).plain.split("\n")[1][0] == braille(0b110111)


def test_colours_and_links_are_carried_in_the_styles():
    page = Page(100, "Test")
    page.write(1, 0, "A", Colour.YELLOW, Colour.BLUE)
    page.write(1, 1, "101", Colour.CYAN, link=101)
    styles = {span.start: span.style for span in page_text(page).spans}
    first, link = styles[0], styles[1]
    assert not isinstance(first, str)
    assert not isinstance(link, str)
    assert (first.color, first.bgcolor) == (
        Color.parse("#ffff00"),
        Color.parse("#0000ff"),
    )
    assert first.meta == {}
    assert link.meta == {"@click": "app.go_to(101)"}
    assert link.underline
