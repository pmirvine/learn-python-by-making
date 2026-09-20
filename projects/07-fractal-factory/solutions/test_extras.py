import pytest
from extras import SUNSET, in_the_main_bulbs, multibrot, quick_mandelbrot

from fractals import mandelbrot


def test_sunset_is_a_palette():
    assert SUNSET(0.0) == (20, 0, 40)
    assert SUNSET(1.0) == (255, 220, 120)


def test_each_multibrot_keeps_its_own_power():
    fields = [multibrot(power) for power in (2, 3, 4)]
    point = -1.2 + 0j
    assert fields[0](point) == 1.0
    assert fields[1](point) < 1.0
    assert fields[0](point) == mandelbrot()(point)


@pytest.mark.parametrize("point", [0j, -1 + 0j, 0.2 + 0.2j, -0.5 + 0.5j])
def test_points_in_the_bulbs(point):
    assert in_the_main_bulbs(point)


@pytest.mark.parametrize("point", [1 + 0j, -1.5 + 0j, 0.3 + 0.6j, -0.1 + 0.9j])
def test_points_outside_the_bulbs(point):
    assert not in_the_main_bulbs(point)


def test_the_short_cut_never_changes_the_answer():
    slow, quick = mandelbrot(60), quick_mandelbrot(60)
    for x in range(-42, 22):
        for y in range(-24, 25):
            point = complex(x / 20, y / 20)
            assert quick(point) == slow(point), point
