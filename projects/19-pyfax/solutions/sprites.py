"""Extend 3: a sprite from Project 15, as teletext graphics, in its own colours.

A graphics character has only one ink. So each takes the colour that most of its
six pixels are, which is what the artists of Ceefax had to do by eye.
"""

from collections import Counter

from pyfax import Cell, Colour, Page
from pyfax.mosaic import pack


def sprite_cells(text: str) -> list[list[Cell]]:
    """Turn the text of a .sprite file into rows of graphics cells."""
    lines = [line for line in text.splitlines() if line and line[0] in ".01234567"]
    cells: list[list[Cell]] = []
    for top, packed in zip(range(0, len(lines), 3), pack(lines), strict=True):
        row: list[Cell] = []
        for column, dots in enumerate(packed):
            patch = "".join(
                line[column * 2 : column * 2 + 2] for line in lines[top : top + 3]
            )
            colours = Counter(patch.replace(".", ""))
            ink = Colour(int(colours.most_common(1)[0][0])) if colours else Colour.WHITE
            row.append(Cell(ink=ink, dots=dots))
        cells.append(row)
    return cells


def stamp(page: Page, row: int, column: int, text: str) -> None:
    """Put a sprite on a page."""
    for down, line in enumerate(sprite_cells(text)):
        page.rows[row + down][column : column + len(line)] = line
