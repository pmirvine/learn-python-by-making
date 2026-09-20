import pytest

from fractals import PALETTES, black_inside, cycled, gradient, steps

BLACK, WHITE, RED = (0, 0, 0), (255, 255, 255), (255, 0, 0)


def test_a_gradient_starts_and_ends_where_it_is_told():
    grey = gradient(BLACK, WHITE)
    assert grey(0.0) == BLACK
    assert grey(1.0) == WHITE
    assert grey(0.5) == (128, 128, 128)


def test_a_gradient_can_have_any_number_of_stops():
    flag = gradient(BLACK, RED, WHITE)
    assert flag(0.5) == RED
    assert flag(0.25) == (128, 0, 0)
    assert flag(0.75) == (255, 128, 128)


def test_a_gradient_ignores_values_out_of_range():
    grey = gradient(BLACK, WHITE)
    assert grey(-3.0) == BLACK
    assert grey(7.0) == WHITE


def test_a_gradient_needs_two_colours():
    with pytest.raises(ValueError, match="at least two"):
        gradient(RED)


def test_steps_do_not_blend():
    bands = steps(BLACK, RED, WHITE)
    assert [bands(v) for v in (0.0, 0.3, 0.4, 0.9, 1.0)] == [
        BLACK,
        BLACK,
        RED,
        WHITE,
        WHITE,
    ]


def test_cycled_runs_through_a_palette_several_times():
    grey = gradient(BLACK, WHITE)
    twice = cycled(grey, 2)
    assert twice(0.25) == grey(0.5)
    assert twice(0.75) == grey(0.5)


def test_black_inside_changes_only_the_top_value():
    palette = black_inside(gradient(RED, WHITE))
    assert palette(1.0) == BLACK
    assert palette(0.0) == RED


@pytest.mark.parametrize("name", PALETTES)
def test_every_palette_gives_proper_colours(name):
    for step in range(101):
        colour = PALETTES[name](step / 100)
        assert len(colour) == 3
        assert all(type(part) is int and 0 <= part <= 255 for part in colour)
