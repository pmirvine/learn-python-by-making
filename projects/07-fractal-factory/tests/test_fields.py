import pytest

from fractals import escape_time, julia, mandelbrot, plasma


def test_zero_never_escapes():
    assert escape_time(0j, 0j, 50) == 1.0


def test_a_distant_point_escapes_at_once():
    assert escape_time(0j, 2 + 2j, 100) == 0.01
    assert escape_time(3 + 0j, 0j, 100) == 0.0


@pytest.mark.parametrize("point", [0j, -1 + 0j, -0.5 + 0.5j, 0.25 + 0j])
def test_points_inside_the_mandelbrot_set(point):
    assert mandelbrot()(point) == 1.0


@pytest.mark.parametrize("point", [1 + 0j, 0.5 + 0.5j, -2.1 + 0j, 1j * 1.1])
def test_points_outside_the_mandelbrot_set(point):
    assert mandelbrot()(point) < 1.0


def test_the_mandelbrot_set_is_symmetrical_about_the_real_axis():
    field = mandelbrot()
    for point in [0.3 + 0.5j, -0.7 + 0.3j, -1.2 + 0.2j]:
        assert field(point) == field(point.conjugate())


def test_a_higher_limit_notices_slower_escapes():
    slow = -0.75 + 0.05j
    assert mandelbrot(limit=20)(slow) == 1.0
    assert mandelbrot(limit=500)(slow) < 1.0


def test_each_julia_set_remembers_its_own_constant():
    calm = julia(0j)
    wild = julia(1 + 0j)
    assert calm(0.5 + 0j) == 1.0
    assert wild(0.5 + 0j) < 1.0
    assert calm(0.5 + 0j) == 1.0


def test_plasma_stays_between_nought_and_one():
    field = plasma()
    for x in range(-20, 21):
        for y in range(-20, 21):
            assert 0.0 <= field(complex(x / 5, y / 5)) <= 1.0
