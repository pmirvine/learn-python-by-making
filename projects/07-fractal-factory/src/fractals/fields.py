"""Fields: the mathematics behind each picture.

A field is a function. You give it a point on the complex plane, and it gives
you a number from 0 to 1. What the number means is up to the field. Nothing in
this module knows about pixels or colours.
"""

import math
from collections.abc import Callable

type Field = Callable[[complex], float]


def escape_time(z: complex, c: complex, limit: int) -> float:
    """Repeat z = z * z + c, and return how soon z escaped, from 0 to 1.

    Once z is further than 2 from the origin, it's never coming back. A point
    that hasn't escaped after `limit` tries scores exactly 1.0.
    """
    for count in range(limit):
        if abs(z) > 2.0:
            return count / limit
        z = z * z + c
    return 1.0


def mandelbrot(limit: int = 100) -> Field:
    """The Mandelbrot set: start from zero, and use the point itself as c."""

    def field(point: complex) -> float:
        return escape_time(0j, point, limit)

    return field


def julia(c: complex, limit: int = 100) -> Field:
    """A Julia set: start from the point, with the same c everywhere."""

    def field(point: complex) -> float:
        return escape_time(point, c, limit)

    return field


def plasma(scale: float = 4.0) -> Field:
    """Four sine waves, added together. No fractal, but very 1980s."""

    def field(point: complex) -> float:
        x, y = point.real * scale, point.imag * scale
        waves = (
            math.sin(x)
            + math.sin(y)
            + math.sin((x + y) / 2)
            + math.sin(math.hypot(x, y))
        )
        return (waves + 4) / 8

    return field
