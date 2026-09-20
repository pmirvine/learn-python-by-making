"""Turning a universe into text. This is the only module that knows what a cell looks like."""

from life.core import Cell

ALIVE = "██"
DEAD = "  "


def render(live: set[Cell], width: int, height: int) -> str:
    """Draw the part of the universe from (0, 0) to (width, height), as text.

    Each cell is two characters wide, because characters in a terminal are
    about twice as tall as they are wide.
    """
    rows = []
    for y in range(height):
        rows.append("".join(ALIVE if (x, y) in live else DEAD for x in range(width)))
    return "\n".join(rows)
