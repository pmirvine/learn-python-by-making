"""The rules of Conway's Game of Life, and nothing else.

A universe is a set of the cells that are alive, each an (x, y) tuple. There
are no edges, and no grid: anywhere that isn't in the set is dead. Nothing in
this module prints, sleeps or knows how big your screen is.
"""

from collections import Counter
from itertools import product

type Cell = tuple[int, int]

_OFFSETS = [(dx, dy) for dx, dy in product((-1, 0, 1), repeat=2) if (dx, dy) != (0, 0)]


def neighbours(cell: Cell) -> list[Cell]:
    """Return the eight cells that surround a cell."""
    x, y = cell
    return [(x + dx, y + dy) for dx, dy in _OFFSETS]


def step(live: set[Cell]) -> set[Cell]:
    """Return the next generation. The set you pass in is left as it was."""
    counts = Counter(neighbour for cell in live for neighbour in neighbours(cell))
    return {
        cell
        for cell, count in counts.items()
        if count == 3 or (count == 2 and cell in live)
    }
