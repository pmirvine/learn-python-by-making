"""Draws a ruler along the bottom of a picture, with a tick every tenth of a unit.

The fix: frange() counts its steps in whole numbers, and never adds floats up.
"""

import math
from collections.abc import Iterator

from PIL import Image


def frange(start: float, stop: float, step: float) -> Iterator[float]:
    """Like range(), but for floats: start, start + step, ... up to but not including stop."""
    # Decide how many values there are, once, in whole numbers. Then work each
    # one out from scratch. Adding `step` on, time after time, lets the tiny
    # error in each addition pile up, until 0.9999999999999999 < 1.0.
    count = math.ceil(round((stop - start) / step, 9))
    for index in range(count):
        yield start + index * step


def tick_columns(width: int, start: float, stop: float, step: float) -> list[int]:
    """Return the pixel column of each tick, for a ruler `width` pixels wide."""
    return [
        round((value - start) / (stop - start) * width)
        for value in frange(start, stop, step)
    ]


def draw_ruler(
    image: Image.Image, start: float, stop: float, step: float = 0.1
) -> None:
    """Draw white ticks, ten pixels high, along the bottom edge of an image."""
    width, height = image.size
    for column in tick_columns(width, start, stop, step):
        for row in range(height - 10, height):
            image.putpixel((column, row), (255, 255, 255))


def main() -> None:
    image = Image.new("RGB", (640, 60))
    draw_ruler(image, 0.0, 0.5)
    print("A ruler from 0 to 0.5: fine.")
    draw_ruler(image, 0.0, 1.0)
    print("A ruler from 0 to 1: fine.")
    image.save("ruler.png")


if __name__ == "__main__":
    main()
