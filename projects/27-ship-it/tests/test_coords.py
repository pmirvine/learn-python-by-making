import pytest

from beeb.screen import to_pixel, to_units


@pytest.mark.parametrize(
    ("x", "y", "expected"),
    [
        (0, 0, (0, 255)),
        (1279, 1023, (159, 0)),
        (640, 512, (80, 127)),
        (7, 3, (0, 255)),
        (8, 4, (1, 254)),
        (-8, 1024, (-1, -1)),
    ],
)
def test_to_pixel_in_mode_2(x, y, expected):
    assert to_pixel(x, y, 160, 256) == expected


def test_to_pixel_accepts_floats_and_returns_ints():
    assert to_pixel(640.7, 511.9, 160, 256) == (80, 128)
    assert all(type(n) is int for n in to_pixel(1.5, 2.5, 160, 256))


def test_to_units_is_the_way_back():
    assert to_units(0, 511, 640, 512) == (0, 0)
    assert to_units(639, 0, 640, 512) == (1278, 1022)


@pytest.mark.parametrize("point", [(0, 0), (640, 512), (1272, 1020)])
def test_round_trip_lands_on_the_same_pixel(point):
    pixel = to_pixel(*point, 160, 256)
    assert to_pixel(*to_units(*pixel, 160, 256), 160, 256) == pixel
