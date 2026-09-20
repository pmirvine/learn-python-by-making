"""Rendering: the only module that knows about pixels, or about Pillow."""

from collections.abc import Callable

from PIL import Image


def render(
    field: Callable[[complex], float],
    size: tuple[int, int] = (640, 480),
    centre: complex = 0j,
    width: float = 4.0,
) -> Image.Image:
    """Paint a field onto a new image, in shades of grey.

    `centre` is the point in the middle of the picture, and `width` is how
    much of the plane the picture spans, from its left edge to its right.
    """
    columns, rows = size
    scale = width / columns

    image = Image.new("L", size)
    for row in range(rows):
        imaginary = (rows / 2 - row) * scale
        for column in range(columns):
            real = (column - columns / 2) * scale
            value = field(centre + complex(real, imaginary))
            image.putpixel((column, row), round(value * 255))
    return image
