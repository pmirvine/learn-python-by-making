"""Patterns to start a universe with: some famous ones, and random soup."""

import random

from life.core import Cell

# Drawn as they look: O is a live cell, and anything else is a dead one.
PATTERNS = {
    "block": """
        OO
        OO
    """,
    "beehive": """
        .OO.
        O..O
        .OO.
    """,
    "blinker": """
        OOO
    """,
    "toad": """
        .OOO
        OOO.
    """,
    "glider": """
        .O.
        ..O
        OOO
    """,
    "lwss": """
        .O..O
        O....
        O...O
        OOOO.
    """,
    "r-pentomino": """
        .OO
        OO.
        .O.
    """,
    "acorn": """
        .O.....
        ...O...
        OO..OOO
    """,
    "gun": """
        ........................O...........
        ......................O.O...........
        ............OO......OO............OO
        ...........O...O....OO............OO
        OO........O.....O...OO..............
        OO........O...O.OO....O.O...........
        ..........O.....O.......O...........
        ...........O...O....................
        ............OO......................
    """,
}


def parse(picture: str) -> set[Cell]:
    """Turn a picture of a pattern into the set of its live cells."""
    rows = [row.strip() for row in picture.strip().splitlines()]
    return {
        (x, y)
        for y, row in enumerate(rows)
        for x, character in enumerate(row)
        if character == "O"
    }


def shift(live: set[Cell], dx: int, dy: int) -> set[Cell]:
    """Return the same pattern, moved across by dx and down by dy."""
    return {(x + dx, y + dy) for x, y in live}


def soup(
    width: int, height: int, density: float = 0.3, seed: int | None = None
) -> set[Cell]:
    """Return a random universe, with roughly `density` of its cells alive."""
    rng = random.Random(seed)
    return {
        (x, y) for x in range(width) for y in range(height) if rng.random() < density
    }
