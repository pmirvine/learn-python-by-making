"""Extend 2: bricks that can't be broken, written as = in a level file.

Only three things change: the table of bricks, what hit_by does to a brick with
no hits to lose, and what `cleared` means. Because `cleared` is a property, the
Game, which asks `level.cleared`, doesn't have to change at all.
"""

from dataclasses import dataclass
from importlib import resources
from pathlib import Path

from pygame import FRect


@dataclass(frozen=True)
class Settings:
    """The numbers that set the feel of the game. They can't be changed once made."""

    width: int = 320
    height: int = 256
    lives: int = 3
    bat_width: float = 40
    bat_speed: float = 260
    ball_size: float = 5
    ball_speed: float = 150
    speed_up: float = 1.02
    top_speed: float = 330


UNBREAKABLE = 0

# What each character of a level file stands for: a colour, points, and hits to break it.
BRICKS = {
    "R": ("red", 50, 1),
    "Y": ("yellow", 30, 1),
    "G": ("green", 10, 1),
    "C": ("cyan", 20, 1),
    "M": ("magenta", 40, 1),
    "W": ("white", 60, 1),
    "#": ("grey", 100, 2),
    "=": ("white", 0, UNBREAKABLE),
}
BRICK_WIDTH, BRICK_HEIGHT = 20, 8
TOP_MARGIN = 24


@dataclass
class Brick:
    rect: FRect
    colour: str
    points: int
    hits: int = 1


class Level:
    """A wall of bricks."""

    def __init__(self, bricks: list[Brick], name: str = "") -> None:
        self.bricks = bricks
        self.name = name

    @classmethod
    def from_text(cls, text: str, name: str = "") -> "Level":
        """Build a level from a picture of it, in which each character is a brick."""
        bricks = []
        for row, line in enumerate(text.strip().splitlines()):
            for column, character in enumerate(line.strip()):
                if character == ".":
                    continue
                if character not in BRICKS:
                    raise ValueError(f"Unknown brick {character!r} in row {row + 1}")
                colour, points, hits = BRICKS[character]
                rect = FRect(
                    column * BRICK_WIDTH,
                    TOP_MARGIN + row * BRICK_HEIGHT,
                    BRICK_WIDTH,
                    BRICK_HEIGHT,
                )
                bricks.append(Brick(rect, colour, points, hits))
        return cls(bricks, name)

    @classmethod
    def from_file(cls, path: Path) -> "Level":
        """Build a level from a text file. The file's name becomes the level's."""
        return cls.from_text(path.read_text(encoding="utf-8"), name=path.stem)

    @classmethod
    def built_in(cls) -> list["Level"]:
        """Return the levels that come with the game, in order."""
        folder = resources.files("breakout") / "levels"
        files = sorted(folder.iterdir(), key=lambda file: file.name)
        return [
            cls.from_text(file.read_text(encoding="utf-8"), name=Path(file.name).stem)
            for file in files
            if file.name.endswith(".txt")
        ]

    @property
    def cleared(self) -> bool:
        """Has everything that can be broken been broken?"""
        return all(brick.hits == UNBREAKABLE for brick in self.bricks)

    def hit_by(self, rect: FRect) -> Brick | None:
        """If the rectangle is touching a brick, hit that brick, and return it."""
        for brick in self.bricks:
            if brick.rect.colliderect(rect):
                if brick.hits != UNBREAKABLE:
                    brick.hits -= 1
                    if brick.hits == 0:
                        self.bricks.remove(brick)
                return brick
        return None

    def __repr__(self) -> str:
        return f"Level({self.name!r}, {len(self.bricks)} bricks)"
