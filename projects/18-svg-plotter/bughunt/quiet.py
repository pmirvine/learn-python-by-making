"""A colleague's plotter never crashes. They're rather proud of that.

    uv run bughunt/quiet.py

It ought to draw a square with a cross in it. Look at quiet.svg in a browser.
"""

from pathlib import Path
from types import TracebackType

from plotter import Plot


class QuietPlot(Plot):
    """The same as yours, but for the way that it leaves a `with`."""

    def __exit__(
        self,
        kind: type[BaseException] | None,
        error: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        self.save()
        return True


def main() -> None:
    with QuietPlot(Path("quiet.svg"), 400, 400) as plot:
        plot.move(50, 50)
        for x, y in [(350, 50), (350, 350), (50, 350), (50, 50)]:
            plot.draw(x, y)
        plot.drawn(350, 350)  # one diagonal...
        plot.move(50, 350)
        plot.draw(350, 50)  # ...and the other
    strokes = plot.svg().count("<path")
    print(f"Finished, with no errors. Strokes in quiet.svg: {strokes}")


if __name__ == "__main__":
    main()
