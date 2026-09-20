"""The game of Breakout: its rules and its state.

Pygame's FRect is used for geometry, which needs no window, so everything in
here can be tested without a screen.
"""

import math
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


# What each character of a level file stands for: a colour, points, and hits to break it.
BRICKS = {
    "R": ("red", 50, 1),
    "Y": ("yellow", 30, 1),
    "G": ("green", 10, 1),
    "C": ("cyan", 20, 1),
    "M": ("magenta", 40, 1),
    "W": ("white", 60, 1),
    "#": ("grey", 100, 2),
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
        return not self.bricks

    def hit_by(self, rect: FRect) -> Brick | None:
        """If the rectangle is touching a brick, hit that brick, and return it."""
        for brick in self.bricks:
            if brick.rect.colliderect(rect):
                brick.hits -= 1
                if brick.hits == 0:
                    self.bricks.remove(brick)
                return brick
        return None

    def __repr__(self) -> str:
        return f"Level({self.name!r}, {len(self.bricks)} bricks)"


class Bat:
    def __init__(self, settings: Settings) -> None:
        self.rect = FRect(0, 0, settings.bat_width, 6)
        self.rect.midbottom = (settings.width / 2, settings.height - 12)
        self.speed = settings.bat_speed
        self.bounds = FRect(0, 0, settings.width, settings.height)

    def move(self, steer: int, seconds: float) -> None:
        """Move left (-1) or right (1), or stay put (0). The bat stops at the walls."""
        self.rect.x += steer * self.speed * seconds
        self.rect.clamp_ip(self.bounds)

    def __repr__(self) -> str:
        return f"Bat(centre={self.rect.centerx:.0f})"


class Ball:
    def __init__(self, size: float, speed: float) -> None:
        self.rect = FRect(0, 0, size, size)
        self.vx = 0.0
        self.vy = -speed

    @property
    def speed(self) -> float:
        """How fast the ball is going, whichever way that is."""
        return math.hypot(self.vx, self.vy)

    @speed.setter
    def speed(self, value: float) -> None:
        if value <= 0:
            raise ValueError(f"A ball's speed must be more than zero, not {value}")
        scale = value / self.speed
        self.vx *= scale
        self.vy *= scale

    def aim(self, offset: float) -> None:
        """Send the ball upwards at its present speed: -1 is hard left, 1 hard right."""
        angle = math.radians(60 * max(-1.0, min(1.0, offset)))
        speed = self.speed
        self.vx = speed * math.sin(angle)
        self.vy = -speed * math.cos(angle)

    def __repr__(self) -> str:
        x, y = self.rect.center
        return f"Ball(at=({x:.0f}, {y:.0f}), velocity=({self.vx:.0f}, {self.vy:.0f}))"
