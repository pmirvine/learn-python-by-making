"""Extend 2: a graph of any function, with axes, ticks and labels.

uv run solutions/chart.py
"""

import math
from collections.abc import Callable
from pathlib import Path

from plotter import Plot

LEFT, BOTTOM, WIDTH, HEIGHT = 140, 120, 1040, 800


def chart(
    plot: Plot,
    function: Callable[[float], float],
    x_range: tuple[float, float],
    y_range: tuple[float, float],
    name: str,
) -> None:
    (x_low, x_high), (y_low, y_high) = x_range, y_range

    def place(x: float, y: float) -> tuple[float, float]:
        """Return where a point of the graph goes on the paper."""
        across = LEFT + (x - x_low) / (x_high - x_low) * WIDTH
        up = BOTTOM + (y - y_low) / (y_high - y_low) * HEIGHT
        return across, up

    plot.pen("gray", width=2)
    plot.move(*place(x_low, 0))
    plot.draw(*place(x_high, 0))
    plot.move(*place(0, y_low))
    plot.draw(*place(0, y_high))
    for tick in range(math.ceil(x_low), math.floor(x_high) + 1):
        x, y = place(tick, 0)
        plot.move(x, y - 10)
        plot.draw(x, y + 10)
        plot.label(x - 10, y - 50, str(tick), size=28)

    plot.pen("yellow", width=4)
    steps = 400
    for step in range(steps + 1):
        x = x_low + (x_high - x_low) * step / steps
        point = place(x, function(x))
        if step == 0:
            plot.move(*point)
        else:
            plot.draw(*point)
    plot.label(LEFT, BOTTOM + HEIGHT + 40, name)


def main() -> None:
    Path("pictures").mkdir(exist_ok=True)
    with Plot(Path("pictures/chart.svg"), title="A damped wave", seconds=5) as plot:
        chart(
            plot,
            lambda x: math.exp(-x / 4) * math.cos(3 * x),
            (-1, 10),
            (-1.2, 1.2),
            "y = exp(-x/4) cos 3x, for -1 < x < 10",
        )


if __name__ == "__main__":
    main()
