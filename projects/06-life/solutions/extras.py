"""The Extend challenges: a universe that wraps round, and a finer way of drawing.

These import from the installed `life` package, exactly as another project would.
"""

from collections import Counter
from collections.abc import Iterator

from life import Cell, neighbours


def step_wrapped(live: set[Cell], width: int, height: int) -> set[Cell]:
    """One generation on a torus: what leaves one edge comes in at the other.

    It's the *neighbours* that have to wrap, before they're counted. Wrapping
    the result of an ordinary step() looks plausible and is wrong: a cell on
    the left edge would have its neighbours counted under two different names,
    (0, y) and (width, y), and neither count would be right.
    """
    counts = Counter(
        (x % width, y % height) for cell in live for x, y in neighbours(cell)
    )
    return {
        cell
        for cell, count in counts.items()
        if count == 3 or (count == 2 and cell in live)
    }


def wrapped(live: set[Cell], width: int, height: int) -> Iterator[set[Cell]]:
    """Like generations(), but for a universe that wraps round."""
    while True:
        yield live
        live = step_wrapped(live, width, height)


# Which character shows a (top, bottom) pair of cells.
HALF_BLOCKS = {
    (False, False): " ",
    (True, False): "▀",
    (False, True): "▄",
    (True, True): "█",
}


def render_fine(live: set[Cell], width: int, height: int) -> str:
    """Draw two rows of cells in each line of text, using half-block characters."""
    rows = []
    for y in range(0, height, 2):
        rows.append(
            "".join(
                HALF_BLOCKS[(x, y) in live, (x, y + 1) in live] for x in range(width)
            )
        )
    return "\n".join(rows)
