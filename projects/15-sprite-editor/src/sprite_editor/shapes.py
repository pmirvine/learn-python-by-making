"""Which cells make up a line, a box, or a patch of one colour."""

from sprite_editor.sprite import Cell, Sprite


def cells_between(start: Cell, end: Cell) -> list[Cell]:
    """Return the cells on a straight line from one cell to another, both included."""
    (x1, y1), (x2, y2) = start, end
    steps = max(abs(x2 - x1), abs(y2 - y1))
    if steps == 0:
        return [start]
    return [
        (round(x1 + (x2 - x1) * n / steps), round(y1 + (y2 - y1) * n / steps))
        for n in range(steps + 1)
    ]


def box(start: Cell, end: Cell) -> list[Cell]:
    """Return the cells round the edge of a rectangle, given two opposite corners."""
    (x1, y1), (x2, y2) = start, end
    left, right = sorted((x1, x2))
    top, bottom = sorted((y1, y2))
    return [
        (x, y)
        for x in range(left, right + 1)
        for y in range(top, bottom + 1)
        if x in (left, right) or y in (top, bottom)
    ]


def flood(sprite: Sprite, start: Cell) -> set[Cell]:
    """Return the cells that join on to `start`, and are the same colour as it."""
    target = sprite[start]
    found: set[Cell] = set()
    waiting = [start]
    while waiting:
        cell = waiting.pop()
        if cell in found or cell not in sprite or sprite[cell] != target:
            continue
        found.add(cell)
        x, y = cell
        waiting += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return found
