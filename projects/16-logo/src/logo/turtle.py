"""The turtle, and the kinds of thing that it can draw on."""

import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

type Point = tuple[float, float]

# The BBC Micro's eight colours, as ever.
COLOURS = ["black", "red", "lime", "yellow", "blue", "magenta", "cyan", "white"]


class Canvas(Protocol):
    """Anything that can draw a line and wipe itself clean will do for a turtle.

    Points are in the turtle's own terms: (0, 0) is the middle, and y goes up.
    """

    def line(self, start: Point, end: Point, colour: int) -> None: ...

    def clear(self) -> None: ...


@dataclass
class Turtle:
    canvas: Canvas
    x: float = 0.0
    y: float = 0.0
    heading: float = 0.0  # in degrees, clockwise from straight up
    pen_down: bool = True
    colour: int = 7

    def forward(self, distance: float) -> None:
        angle = math.radians(self.heading)
        start = (self.x, self.y)
        self.x += distance * math.sin(angle)
        self.y += distance * math.cos(angle)
        if self.pen_down:
            self.canvas.line(start, (self.x, self.y), self.colour)

    def goto(self, x: float, y: float) -> None:
        start = (self.x, self.y)
        self.x, self.y = x, y
        if self.pen_down:
            self.canvas.line(start, (x, y), self.colour)

    def turn(self, degrees: float) -> None:
        self.heading = (self.heading + degrees) % 360

    def home(self) -> None:
        self.x = self.y = self.heading = 0.0


@dataclass
class Recorder:
    """A canvas that writes down what it was asked to draw. It's for tests."""

    lines: list[tuple[Point, Point, int]] = field(default_factory=list)

    def line(self, start: Point, end: Point, colour: int) -> None:
        self.lines.append((start, end, colour))

    def clear(self) -> None:
        self.lines.clear()


@dataclass
class SvgCanvas(Recorder):
    """A canvas that can save itself as a picture, for a browser to show."""

    size: int = 600

    def save(self, path: Path) -> None:
        half = self.size / 2
        shapes = [
            f'<line x1="{half + x1:.1f}" y1="{half - y1:.1f}" '
            f'x2="{half + x2:.1f}" y2="{half - y2:.1f}" stroke="{COLOURS[colour]}"/>'
            for (x1, y1), (x2, y2), colour in self.lines
        ]
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.size}" '
            f'height="{self.size}" style="background: black" stroke-linecap="round">\n'
            + "\n".join(shapes)
            + "\n</svg>\n"
        )
        path.write_text(svg, encoding="utf-8")
