"""The failing tests that pin the ruler's bug down. Try them on bughunt/ruler.py."""

import pytest
from PIL import Image
from ruler import draw_ruler, frange, tick_columns


@pytest.mark.parametrize(
    ("stop", "step", "count"),
    [(0.5, 0.1, 5), (1.0, 0.1, 10), (2.0, 0.1, 20), (1.0, 0.25, 4), (1.0, 0.3, 4)],
)
def test_frange_stops_before_the_stop(stop, step, count):
    values = list(frange(0.0, stop, step))
    assert len(values) == count
    assert all(value < stop - 1e-9 for value in values)


def test_frange_values_are_where_they_should_be():
    assert list(frange(0.0, 1.0, 0.1)) == pytest.approx([n / 10 for n in range(10)])


def test_every_tick_is_on_the_ruler():
    assert all(0 <= column < 640 for column in tick_columns(640, 0.0, 1.0, 0.1))


def test_a_whole_ruler_can_be_drawn():
    image = Image.new("RGB", (640, 60))
    draw_ruler(image, 0.0, 1.0)
    assert image.getpixel((64, 55)) == (255, 255, 255)
