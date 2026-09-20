import pytest

from life import PATTERNS, parse, shift, soup


def test_parse_reads_a_picture():
    picture = """
        .O.
        ..O
        OOO
    """
    assert parse(picture) == {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)}


@pytest.mark.parametrize("name", PATTERNS)
def test_every_pattern_has_some_cells_and_starts_in_the_corner(name):
    cells = parse(PATTERNS[name])
    assert cells
    assert min(x for x, _ in cells) == 0
    assert min(y for _, y in cells) == 0


def test_shift():
    assert shift({(0, 0), (1, 2)}, 10, -1) == {(10, -1), (11, 1)}


def test_soup_is_repeatable_with_a_seed():
    assert soup(20, 10, seed=1) == soup(20, 10, seed=1)
    assert soup(20, 10, seed=1) != soup(20, 10, seed=2)


@pytest.mark.parametrize("density", [0.1, 0.5, 0.9])
def test_soup_is_about_as_thick_as_you_ask(density):
    cells = soup(100, 100, density=density, seed=3)
    assert len(cells) == pytest.approx(10_000 * density, rel=0.1)
    assert all(0 <= x < 100 and 0 <= y < 100 for x, y in cells)
