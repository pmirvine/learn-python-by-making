"""Animating a universe in the terminal."""

import time
from itertools import islice

from life.core import generations
from life.render import render

HOME = "\033[H"
CLEAR = "\033[2J"

GLIDER = {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)}


def main() -> None:
    print(CLEAR, end="")
    for number, universe in enumerate(islice(generations(GLIDER), 100)):
        print(HOME + render(universe, 40, 20))
        print(f"Generation {number}, population {len(universe)}  ")
        time.sleep(0.1)
