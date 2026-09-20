"""Fields: the mathematics behind each picture.

A field is a function. You give it a point on the complex plane, and it gives
you a number from 0 to 1. What the number means is up to the field. Nothing in
this module knows about pixels or colours.
"""

import math


def mandelbrot(point: complex, limit: int = 100) -> float:
    """Repeat z = z * z + point, and return how soon z escaped, from 0 to 1.

    Once z is further than 2 from the origin, it's never coming back. A point
    that hasn't escaped after `limit` tries scores exactly 1.0.
    """
    z = 0j
    for count in range(limit):
        if abs(z) > 2.0:
            return count / limit
        z = z * z + point
    return 1.0


def plasma(point: complex) -> float:
    """Four sine waves, added together. No fractal, but very 1980s."""
    x, y = point.real * 4, point.imag * 4
    waves = (
        math.sin(x) + math.sin(y) + math.sin((x + y) / 2) + math.sin(math.hypot(x, y))
    )
    return (waves + 4) / 8
