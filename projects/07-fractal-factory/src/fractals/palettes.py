"""Palettes: turning a number from 0 to 1 into a colour.

A palette is a function too. It takes a float, and returns (red, green, blue).
"""

from collections.abc import Callable

type Colour = tuple[int, int, int]
type Palette = Callable[[float], Colour]

BLACK = (0, 0, 0)


def gradient(*stops: Colour) -> Palette:
    """Return a palette that fades smoothly through any number of colours."""
    if len(stops) < 2:
        raise ValueError("A gradient needs at least two colours.")

    def palette(value: float) -> Colour:
        position = min(max(value, 0.0), 1.0) * (len(stops) - 1)
        index = min(int(position), len(stops) - 2)
        blend = position - index
        (r1, g1, b1), (r2, g2, b2) = stops[index], stops[index + 1]
        return (
            round(r1 + (r2 - r1) * blend),
            round(g1 + (g2 - g1) * blend),
            round(b1 + (b2 - b1) * blend),
        )

    return palette


def steps(*colours: Colour) -> Palette:
    """Return a palette of flat bands, with no fading between them."""

    def palette(value: float) -> Colour:
        index = min(int(value * len(colours)), len(colours) - 1)
        return colours[max(index, 0)]

    return palette


def cycled(palette: Palette, times: int) -> Palette:
    """Return a palette that runs through another one several times over."""

    def cycling(value: float) -> Colour:
        return palette(value * times % 1.0)

    return cycling


def black_inside(palette: Palette) -> Palette:
    """Return a palette that paints 1.0, 'never escaped', black."""

    def painting(value: float) -> Colour:
        return BLACK if value >= 1.0 else palette(value)

    return painting


PALETTES: dict[str, Palette] = {
    "fire": gradient(
        BLACK, (128, 0, 0), (255, 128, 0), (255, 255, 128), (255, 255, 255)
    ),
    "ocean": gradient(
        (0, 7, 100), (32, 107, 203), (237, 255, 255), (255, 170, 0), (0, 2, 0)
    ),
    "grey": gradient(BLACK, (255, 255, 255)),
    "beeb": steps(
        (255, 0, 0),
        (255, 255, 0),
        (0, 255, 0),
        (0, 255, 255),
        (0, 0, 255),
        (255, 0, 255),
        (255, 255, 255),
    ),
}
