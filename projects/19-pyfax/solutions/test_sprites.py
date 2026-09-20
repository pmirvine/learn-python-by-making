from sprites import sprite_cells, stamp

from pyfax import Colour, Page

ROCKET = """\
# A rocket
sprite 4 6
.77.
.77.
7667
7667
1331
3..3
"""


def test_each_character_takes_the_colour_that_most_of_its_pixels_are():
    top, bottom = sprite_cells(ROCKET)
    assert [cell.dots for cell in top] == [0b111010, 0b110101]
    assert [cell.ink for cell in top] == [Colour.WHITE, Colour.WHITE]
    assert [cell.dots for cell in bottom] == [0b011111, 0b101111]
    assert bottom[0].ink in (Colour.WHITE, Colour.CYAN, Colour.RED, Colour.YELLOW)


def test_stamping_a_sprite_on_a_page():
    page = Page(501, "Rocket")
    stamp(page, 10, 5, ROCKET)
    assert page.rows[10][5].dots == 0b111010
    assert page.rows[11][6].dots == 0b101111
    assert page.rows[10][7].dots is None
