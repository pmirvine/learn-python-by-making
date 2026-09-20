"""What this front end needs from a game, and nothing more.

This module is the front end's half of a bargain. It imports no game, and no
game has to import it: anything with these methods will do.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, runtime_checkable


class Game(Protocol):
    """Something that can be played by typing at it."""

    @property
    def title(self) -> str: ...

    @property
    def over(self) -> bool: ...

    def opening(self) -> str:
        """Return what the player reads first."""
        ...

    def play(self, text: str) -> str:
        """Take one turn, and return the reply."""
        ...

    def status(self) -> dict[str, str]:
        """Return a few facts worth keeping in view, such as the number of moves."""
        ...


@dataclass(frozen=True, slots=True)
class Place:
    """A room on the map. `exits` holds letters from "nsewud"."""

    label: str
    x: int
    y: int
    floor: int = 0
    exits: str = ""


@dataclass(frozen=True, slots=True)
class Chart:
    """As much of the map as the player has seen, and where they are on it."""

    places: tuple[Place, ...]
    here: Place
    caption: str = ""


@runtime_checkable
class Mapped(Protocol):
    """A game that can say where the player has been."""

    def chart(self) -> Chart: ...


@runtime_checkable
class Undoable(Protocol):
    """A game that can take a move back."""

    def undo(self) -> str: ...


@runtime_checkable
class Saveable(Protocol):
    """A game that can be put away in a file, and got out again."""

    def save(self, path: Path) -> str: ...

    def restore(self, path: Path) -> str: ...
