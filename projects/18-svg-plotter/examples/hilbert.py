"""A Hilbert curve: one line that visits every cell of a grid, and never crosses itself."""

from collections.abc import Iterator
from pathlib import Path

from plotter import Plot

PICTURES = Path("pictures")
PICTURES.mkdir(exist_ok=True)


def hilbert(order: int, corner: complex, a: complex, b: complex) -> Iterator[complex]:
    """Yield the points of the curve that fills the box at `corner` with sides a and b.

    The points are complex numbers, as in Project 7: x is the real part, and y the
    imaginary part, which makes "half of this side" and "minus that one" easy to say.
    """
    if order == 0:
        yield corner + (a + b) / 2
        return
    yield from hilbert(order - 1, corner, b / 2, a / 2)
    yield from hilbert(order - 1, corner + a / 2, a / 2, b / 2)
    yield from hilbert(order - 1, corner + a / 2 + b / 2, a / 2, b / 2)
    yield from hilbert(order - 1, corner + a / 2 + b, -b / 2, -a / 2)


with Plot(PICTURES / "hilbert.svg", 1024, 1024, title="Hilbert", seconds=12) as plot:
    plot.pen("lime", width=4)
    first, *rest = hilbert(5, 32 + 32j, 960, 960j)
    plot.move(first.real, first.imag)
    for point in rest:
        plot.draw(point.real, point.imag)
