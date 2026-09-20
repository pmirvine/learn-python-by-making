"""A sprite: a small picture in eight colours, with see-through parts."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

type Cell = tuple[int, int]
type Colour = int | None  # 0 to 7 are the BBC Micro's colours. None is see-through.

COLOURS = 8
CLEAR = "."


class SpriteError(ValueError):
    """A sprite file that doesn't make sense."""


@dataclass
class Sprite:
    width: int
    height: int
    pixels: dict[Cell, int] = field(default_factory=dict)

    def __contains__(self, cell: Cell) -> bool:
        x, y = cell
        return 0 <= x < self.width and 0 <= y < self.height

    def __getitem__(self, cell: Cell) -> Colour:
        return self.pixels.get(cell)

    def __setitem__(self, cell: Cell, colour: Colour) -> None:
        if cell not in self:
            raise IndexError(f"{cell} isn't in a {self.width} by {self.height} sprite")
        if colour is None:
            self.pixels.pop(cell, None)
        else:
            self.pixels[cell] = colour

    def to_text(self) -> str:
        rows = [
            "".join(
                CLEAR if self[x, y] is None else str(self[x, y])
                for x in range(self.width)
            )
            for y in range(self.height)
        ]
        return "\n".join([f"sprite {self.width} {self.height}", *rows]) + "\n"

    @classmethod
    def from_text(cls, text: str) -> Self:
        lines = [line.strip() for line in text.splitlines()]
        lines = [line for line in lines if line and not line.startswith("#")]
        match lines[0].split() if lines else []:
            case ["sprite", width, height] if width.isdecimal() and height.isdecimal():
                sprite = cls(int(width), int(height))
            case _:
                raise SpriteError("the first line should be like: sprite 16 16")

        rows = lines[1:]
        if len(rows) != sprite.height:
            raise SpriteError(f"there are {len(rows)} rows, and not {sprite.height}")
        for y, row in enumerate(rows):
            if len(row) != sprite.width:
                raise SpriteError(f"row {y} is {len(row)} long, and not {sprite.width}")
            for x, character in enumerate(row):
                if character == CLEAR:
                    continue
                if character not in "01234567":
                    raise SpriteError(f"row {y} has a {character!r} in it")
                sprite[x, y] = int(character)
        return sprite

    def save(self, path: Path) -> None:
        path.write_text(self.to_text(), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> Self:
        return cls.from_text(path.read_text(encoding="utf-8"))
