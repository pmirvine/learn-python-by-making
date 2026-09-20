"""A rose: one curve, seven petals wide, that closes after five turns."""

import math
from pathlib import Path

from plotter import Plot

PICTURES = Path("pictures")
PICTURES.mkdir(exist_ok=True)

with Plot(PICTURES / "rose.svg", title="A rose", seconds=8) as plot:
    plot.pen("hotpink", width=3)
    plot.move(1040, 512)
    for step in range(1, 2001):
        angle = step / 2000 * 5 * math.tau
        radius = 400 * math.cos(angle * 7 / 5)
        plot.draw(640 + radius * math.cos(angle), 512 + radius * math.sin(angle))
    plot.pen("white")
    plot.label(40, 40, "r = cos(7θ/5), for 0 < θ < 10π")
