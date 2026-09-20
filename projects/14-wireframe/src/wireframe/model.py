"""Ships: what they're made of, and how to read one from a TOML file."""

import tomllib
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path

from wireframe.vec3 import Vec3


class ModelError(ValueError):
    """A ship file that can be read, and doesn't make sense."""


@dataclass(frozen=True, slots=True)
class Face:
    points: tuple[int, ...]
    colour: str = "white"


@dataclass(frozen=True, slots=True)
class Ship:
    name: str
    points: tuple[Vec3, ...]
    faces: tuple[Face, ...]

    @property
    def radius(self) -> float:
        """How far the furthest point is from the middle."""
        return max(abs(point) for point in self.points)


def point(entry: object, where: str) -> Vec3:
    match entry:
        case [int() | float() as x, int() | float() as y, int() | float() as z]:
            return Vec3(x, y, z)
        case _:
            raise ModelError(f"{where} should be three numbers, and it's {entry!r}")


def face(entry: object, where: str, count: int) -> Face:
    match entry:
        case {"points": [int(), int(), int(), *_] as corners, "colour": str(colour)}:
            pass
        case {"points": [int(), int(), int(), *_] as corners, **others} if not others:
            colour = "white"
        case _:
            raise ModelError(
                f"{where} needs points, which are three or more whole numbers, "
                "and it may have a colour, which is a name"
            )
    for corner in corners:
        if not 0 <= corner < count:
            raise ModelError(f"{where} uses point {corner}, and there's no such point")
    return Face(tuple(corners), colour)


def parse(text: str) -> Ship:
    """Make a ship from the text of a TOML file."""
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as error:
        raise ModelError(f"that isn't TOML: {error}") from error

    match data:
        case {"name": str(name), "points": [*points], "faces": [*faces]}:
            corners = tuple(
                point(entry, f"point {number}") for number, entry in enumerate(points)
            )
            sides = tuple(
                face(entry, f"face {number}", len(corners))
                for number, entry in enumerate(faces)
            )
            return Ship(name, corners, sides)
        case _:
            raise ModelError("a ship needs a name, some points, and some [[faces]]")


def load(path: Path) -> Ship:
    return parse(path.read_text(encoding="utf-8"))


def hangar() -> list[Ship]:
    """Return the ships that come with the program, in order of name."""
    folder = files("wireframe") / "ships"
    ships = [
        parse(entry.read_text(encoding="utf-8"))
        for entry in folder.iterdir()
        if entry.name.endswith(".toml")
    ]
    return sorted(ships, key=lambda ship: ship.name)
