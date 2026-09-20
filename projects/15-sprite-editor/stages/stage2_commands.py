"""Things that can be done to a sprite, and undone again."""

from abc import ABC, abstractmethod

from sprite_editor.sprite import Cell, Colour, Sprite


class Command(ABC):
    """One change to a sprite, which knows how to put things back."""

    label = "Change"

    @abstractmethod
    def do(self, sprite: Sprite) -> None:
        """Make the change."""

    @abstractmethod
    def undo(self, sprite: Sprite) -> None:
        """Put things back as they were before `do`."""

    def __str__(self) -> str:
        return self.label


class Paint(Command):
    """Set some pixels. Every tool that draws ends up as one of these."""

    def __init__(self, label: str, sprite: Sprite, changes: dict[Cell, Colour]) -> None:
        self.label = label
        self.after = {cell: ink for cell, ink in changes.items() if cell in sprite}
        self.before = {cell: sprite[cell] for cell in self.after}

    def do(self, sprite: Sprite) -> None:
        for cell, colour in self.after.items():
            sprite[cell] = colour

    def undo(self, sprite: Sprite) -> None:
        for cell, colour in self.before.items():
            sprite[cell] = colour

    def __bool__(self) -> bool:
        """A command that would change nothing isn't worth remembering."""
        return self.before != self.after


class Flip(Command):
    """Swap left with right. It needs to remember nothing: doing it twice undoes it."""

    label = "Flip"

    def do(self, sprite: Sprite) -> None:
        last = sprite.width - 1
        sprite.pixels = {(last - x, y): c for (x, y), c in sprite.pixels.items()}

    def undo(self, sprite: Sprite) -> None:
        self.do(sprite)


class Shift(Command):
    """Slide the whole picture along, with whatever falls off one side joining the other."""

    def __init__(self, dx: int, dy: int) -> None:
        self.label = f"Shift {dx:+}, {dy:+}"
        self.dx = dx
        self.dy = dy

    def do(self, sprite: Sprite) -> None:
        slide(sprite, self.dx, self.dy)

    def undo(self, sprite: Sprite) -> None:
        slide(sprite, -self.dx, -self.dy)


def slide(sprite: Sprite, dx: int, dy: int) -> None:
    sprite.pixels = {
        ((x + dx) % sprite.width, (y + dy) % sprite.height): colour
        for (x, y), colour in sprite.pixels.items()
    }


class History:
    """What's been done, so that it can be undone, and what's been undone, likewise."""

    def __init__(self, sprite: Sprite) -> None:
        self.sprite = sprite
        self.done: list[Command] = []
        self.undone: list[Command] = []

    def __str__(self) -> str:
        return f"{len(self.done)} done, {len(self.undone)} undone"

    def perform(self, command: Command) -> None:
        command.do(self.sprite)
        self.done.append(command)
        self.undone.clear()

    def undo(self) -> None:
        if not self.done:
            return
        command = self.done.pop()
        command.undo(self.sprite)
        self.undone.append(command)

    def redo(self) -> None:
        if not self.undone:
            return
        command = self.undone.pop()
        command.do(self.sprite)
        self.done.append(command)
