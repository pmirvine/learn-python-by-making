"""Extend 1 and 2: two more shapes, which are one method each, and a quarter turn."""

from sprite_editor.commands import Command
from sprite_editor.sprite import Cell, Sprite
from sprite_editor.tools import ShapeTool


class FilledBox(ShapeTool):
    name = "Block"
    key = "k"

    def cells(self, start: Cell, end: Cell) -> list[Cell]:
        (x1, y1), (x2, y2) = start, end
        return [
            (x, y)
            for x in range(min(x1, x2), max(x1, x2) + 1)
            for y in range(min(y1, y2), max(y1, y2) + 1)
        ]


class Ellipse(ShapeTool):
    name = "Oval"
    key = "o"

    def cells(self, start: Cell, end: Cell) -> list[Cell]:
        (x1, y1), (x2, y2) = start, end
        middle_x, middle_y = (x1 + x2) / 2, (y1 + y2) / 2
        radius_x, radius_y = abs(x2 - x1) / 2 + 0.5, abs(y2 - y1) / 2 + 0.5

        def inside(x: int, y: int) -> bool:
            across = (x - middle_x) / radius_x
            down = (y - middle_y) / radius_y
            return across**2 + down**2 <= 1

        # A cell is on the edge if it's inside, and one of its neighbours isn't.
        return [
            (x, y)
            for x in range(min(x1, x2), max(x1, x2) + 1)
            for y in range(min(y1, y2), max(y1, y2) + 1)
            if inside(x, y)
            and not all(
                inside(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
            )
        ]


class Turn(Command):
    """A quarter turn clockwise, for a square sprite. Undoing it is three more."""

    label = "Turn"

    def do(self, sprite: Sprite) -> None:
        if sprite.width != sprite.height:
            raise ValueError("only a square sprite can be turned where it stands")
        last = sprite.height - 1
        sprite.pixels = {(last - y, x): c for (x, y), c in sprite.pixels.items()}

    def undo(self, sprite: Sprite) -> None:
        for _ in range(3):
            self.do(sprite)
