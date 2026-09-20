"""The things that the mouse can do to a picture."""

import logging
from abc import ABC, abstractmethod
from collections.abc import Callable

from sprite_editor.commands import Command, Paint
from sprite_editor.shapes import box, cells_between, flood
from sprite_editor.sprite import Cell, Colour, Sprite

log = logging.getLogger(__name__)


class Tool(ABC):
    """A tool gathers up some changes while the button is down.

    It never touches the sprite itself. When the button comes up, it hands back
    a command, and the command does the work, so that everything can be undone.
    """

    name = "Tool"
    key = "?"

    def __init__(self) -> None:
        self.changes: dict[Cell, Colour] = {}
        self.colour: Colour = None
        self.start: Cell = (0, 0)

    def press(self, sprite: Sprite, cell: Cell, colour: Colour) -> None:
        self.changes = {}
        self.colour = colour
        self.start = cell
        self.drag(sprite, cell)

    @abstractmethod
    def drag(self, sprite: Sprite, cell: Cell) -> None:
        """The pointer is over this cell now, with the button still down."""

    def release(self, sprite: Sprite) -> Command | None:
        command = Paint(self.name, sprite, self.changes)
        self.changes = {}
        return command or None


class Pencil(Tool):
    name = "Pencil"
    key = "p"

    def __init__(self) -> None:
        super().__init__()
        self.last: Cell = (0, 0)

    def press(self, sprite: Sprite, cell: Cell, colour: Colour) -> None:
        self.last = cell
        super().press(sprite, cell, colour)

    def drag(self, sprite: Sprite, cell: Cell) -> None:
        for step in cells_between(self.last, cell):
            self.changes[step] = self.colour
        self.last = cell


class Eraser(Pencil):
    name = "Eraser"
    key = "e"

    def press(self, sprite: Sprite, cell: Cell, colour: Colour) -> None:
        super().press(sprite, cell, None)


class ShapeTool(Tool):
    """A tool that stretches a shape from where the button went down to where it is."""

    def drag(self, sprite: Sprite, cell: Cell) -> None:
        self.changes = dict.fromkeys(self.cells(self.start, cell), self.colour)

    @abstractmethod
    def cells(self, start: Cell, end: Cell) -> list[Cell]:
        """Return the cells of the shape."""


class Line(ShapeTool):
    name = "Line"
    key = "l"

    def cells(self, start: Cell, end: Cell) -> list[Cell]:
        return cells_between(start, end)


class Box(ShapeTool):
    name = "Box"
    key = "b"

    def cells(self, start: Cell, end: Cell) -> list[Cell]:
        return box(start, end)


class Bucket(Tool):
    name = "Fill"
    key = "f"

    def drag(self, sprite: Sprite, cell: Cell) -> None:
        patch = flood(sprite, cell) if cell in sprite else set()
        self.changes = dict.fromkeys(patch, self.colour)


class Picker(Tool):
    """Pick up a colour from the picture. It changes nothing, and so there's no command."""

    name = "Pick"
    key = "i"

    def __init__(self, on_pick: Callable[[Colour], None]) -> None:
        super().__init__()
        self.on_pick = on_pick

    def drag(self, sprite: Sprite, cell: Cell) -> None:
        if cell in sprite:
            log.debug("Picked %s at %s", sprite[cell], cell)
            self.on_pick(sprite[cell])

    def release(self, sprite: Sprite) -> Command | None:
        return None
