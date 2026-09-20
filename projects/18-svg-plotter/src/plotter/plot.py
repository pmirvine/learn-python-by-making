"""A pen plotter that draws on a file: MOVE and DRAW, for the browser."""

import math
from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from string.templatelib import Template
from types import TracebackType
from typing import Self

from plotter.markup import Safe, render

type Point = tuple[float, float]
type Element = Stroke | Label | Group  # a `type` statement may mention what comes later


@dataclass
class Stroke:
    """One unbroken line, from where the pen went down to where it came up."""

    points: list[Point]
    colour: str
    width: float

    @property
    def length(self) -> float:
        return sum(math.dist(a, b) for a, b in zip(self.points, self.points[1:]))


@dataclass
class Label:
    at: Point
    words: str
    size: float
    colour: str


@dataclass
class Group:
    """Some elements that are moved, turned or scaled together."""

    transform: str
    children: list[Element] = field(default_factory=list[Element])


class Plot:
    """A sheet of paper, with the origin at the bottom left, as on the BBC Micro.

    Use it in a `with`, and the file is written when the block finishes:

        with Plot(Path("square.svg")) as plot:
            plot.move(100, 100)
            plot.draw(400, 100)
    """

    def __init__(
        self,
        path: Path,
        width: int = 1280,
        height: int = 1024,
        paper: str = "black",
        title: str = "",
        seconds: float = 0.0,
    ) -> None:
        self.path = path
        self.width = width
        self.height = height
        self.paper = paper
        self.title = title or path.stem
        self.seconds = seconds  # how long the picture takes to draw itself, if at all
        self.colour = "white"
        self.pen_width = 2.0
        self.position: Point = (0.0, 0.0)
        self.stroke: Stroke | None = None
        self.open_groups: list[Group] = [Group("")]

    # Being a context manager.

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        kind: type[BaseException] | None,
        error: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if kind is None:
            self.save()

    # Drawing.

    def move(self, x: float, y: float) -> None:
        """Lift the pen, and go somewhere."""
        self.position = (x, y)
        self.stroke = None

    def draw(self, x: float, y: float) -> None:
        """Put the pen down, if it's up, and draw a line to somewhere."""
        if self.stroke is None:
            self.stroke = Stroke([self.position], self.colour, self.pen_width)
            self.open_groups[-1].children.append(self.stroke)
        self.stroke.points.append((x, y))
        self.position = (x, y)

    def pen(self, colour: str, width: float | None = None) -> None:
        """Change pens. Whatever is drawn next is a new stroke."""
        self.colour = colour
        if width is not None:
            self.pen_width = width
        self.stroke = None

    def label(self, x: float, y: float, words: str, size: float = 32) -> None:
        self.open_groups[-1].children.append(Label((x, y), words, size, self.colour))

    @contextmanager
    def turned(self, degrees: float, about: Point) -> Generator[None]:
        """Whatever is drawn inside the `with` is turned anticlockwise about a point."""
        x, y = self.on_paper(about)
        group = Group(f"rotate({-degrees:g} {x:g} {y:g})")
        self.open_groups[-1].children.append(group)
        self.open_groups.append(group)
        self.stroke = None
        try:
            yield
        finally:
            self.open_groups.pop()
            self.stroke = None

    # Turning it all into SVG.

    def on_paper(self, point: Point) -> Point:
        """SVG measures y downwards from the top. Everybody else measures it upwards."""
        return point[0], self.height - point[1]

    def svg(self) -> str:
        inked = sum(stroke.length for stroke in self.strokes(self.open_groups[0]))
        self.drawn = 0.0
        body = [self.element(child, inked) for child in self.open_groups[0].children]
        style = ANIMATION if self.seconds else Safe("")
        return render(
            t"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}"
     fill="none" stroke-linecap="round" stroke-linejoin="round">
<title>{self.title}</title>
<style>{style}</style>
<rect width="100%" height="100%" fill="{self.paper}"/>
{body}</svg>
"""
        )

    def strokes(self, group: Group) -> Generator[Stroke]:
        for child in group.children:
            match child:
                case Stroke():
                    yield child
                case Group():
                    yield from self.strokes(child)
                case Label():
                    pass

    def element(self, item: Element, inked: float) -> Template:
        match item:
            case Stroke(points, colour, width):
                path = "M" + " L".join(
                    f"{x:.1f} {y:.1f}" for x, y in map(self.on_paper, points)
                )
                delay = self.seconds * self.drawn / inked if inked else 0.0
                taken = self.seconds * item.length / inked if inked else 0.0
                self.drawn += item.length
                timing = f"animation-delay:{delay:.2f}s;animation-duration:{taken:.2f}s"
                return t'<path d="{path}" stroke="{colour}" stroke-width="{width:g}" pathLength="1" style="{timing}"/>\n'
            case Label((x, y), words, size, colour):
                x, y = self.on_paper((x, y))
                return t'<text x="{x:.1f}" y="{y:.1f}" font-size="{size:g}" font-family="monospace" fill="{colour}">{words}</text>\n'
            case Group(transform, children):
                inside = [self.element(child, inked) for child in children]
                return t'<g transform="{transform}">\n{inside}</g>\n'

    def save(self) -> None:
        self.path.write_text(self.svg(), encoding="utf-8")


ANIMATION = Safe("""
path { stroke-dasharray: 1; stroke-dashoffset: 1; animation: draw linear forwards; }
@keyframes draw { to { stroke-dashoffset: 0; } }
""")
