"""Rendering: the only module that knows about pixels, or about Pillow."""

from PIL import Image

from fractals.fields import Field
from fractals.palettes import Palette


def render(
    field: Field,
    palette: Palette,
    *,
    size: tuple[int, int] = (640, 480),
    centre: complex = 0j,
    width: float = 4.0,
) -> Image.Image:
    """Paint a field, through a palette, onto a new image.

    `centre` is the point in the middle of the picture, and `width` is how
    much of the plane the picture spans, from its left edge to its right.
    """
    columns, rows = size
    scale = width / columns

    image = Image.new("RGB", size)
    for row in range(rows):
        imaginary = (rows / 2 - row) * scale
        for column in range(columns):
            real = (column - columns / 2) * scale
            value = field(centre + complex(real, imaginary))
            image.putpixel((column, row), palette(value))
    return image
