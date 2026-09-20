"""A pen plotter that draws on a file. (Stage 1: strings, stuck together.)"""

from pathlib import Path

type Point = tuple[float, float]


class Plot:
    def __init__(self, path: Path, width: int = 1280, height: int = 1024) -> None:
        self.path = path
        self.width = width
        self.height = height
        self.colour = "white"
        self.position: Point = (0.0, 0.0)
        self.parts: list[str] = []

    def move(self, x: float, y: float) -> None:
        self.position = (x, y)

    def draw(self, x: float, y: float) -> None:
        x1, y1 = self.position
        self.parts.append(
            f'<line x1="{x1:.1f}" y1="{self.height - y1:.1f}" '
            f'x2="{x:.1f}" y2="{self.height - y:.1f}" stroke="{self.colour}"/>'
        )
        self.position = (x, y)

    def label(self, x: float, y: float, words: str, size: float = 32) -> None:
        self.parts.append(
            f'<text x="{x:.1f}" y="{self.height - y:.1f}" font-size="{size:g}" '
            f'font-family="monospace" fill="{self.colour}">{words}</text>'
        )

    def svg(self) -> str:
        body = "\n".join(self.parts)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {self.width} {self.height}" stroke-width="2">\n'
            f'<rect width="100%" height="100%" fill="black"/>\n{body}\n</svg>\n'
        )

    def save(self) -> None:
        self.path.write_text(self.svg(), encoding="utf-8")
