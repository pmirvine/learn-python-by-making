"""10 PRINT CHR$(205.5+RND(1)); : GOTO 10 -- the most famous one-liner in BASIC."""

import random
from pathlib import Path

from plotter import Plot

PICTURES = Path("pictures")
PICTURES.mkdir(exist_ok=True)
SIZE = 32
rng = random.Random(10)

with Plot(PICTURES / "maze.svg", paper="#4040e0", title="10 PRINT") as plot:
    plot.pen("#a0a0ff", width=6)
    for y in range(0, 1024, SIZE):
        for x in range(0, 1280, SIZE):
            if rng.random() < 0.5:
                plot.move(x, y)
                plot.draw(x + SIZE, y + SIZE)
            else:
                plot.move(x, y + SIZE)
                plot.draw(x + SIZE, y)
