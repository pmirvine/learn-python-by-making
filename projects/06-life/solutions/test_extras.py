from itertools import islice

from extras import render_fine, wrapped

from life import PATTERNS, parse, shift


def test_a_glider_goes_off_one_edge_and_comes_back_on_the_other():
    glider = parse(PATTERNS["glider"])
    # A glider moves one cell diagonally every 4 generations, so in a 10 by 10
    # world it's back where it started after 40.
    later = next(islice(wrapped(glider, 10, 10), 40, None))
    assert later == glider


def test_wrapped_keeps_every_cell_inside():
    for universe in islice(wrapped(parse(PATTERNS["acorn"]), 12, 8), 60):
        assert all(0 <= x < 12 and 0 <= y < 8 for x, y in universe)


def test_render_fine_packs_two_rows_into_one_line():
    cells = {(0, 0), (1, 1), (2, 0), (2, 1)}
    assert render_fine(cells, 4, 2) == "▀▄█ "


def test_render_fine_of_a_shifted_block():
    block = shift(parse(PATTERNS["block"]), 1, 1)
    assert render_fine(block, 4, 4) == " ▄▄ \n ▀▀ "
