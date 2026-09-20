"""A universe with a clock: it can run, pause and step, and it can be drawn on."""

import time
from collections.abc import Iterable

from life import Cell, shift, step

FRAME_BUDGET = 1 / 30  # seconds: the most that one update() should spend on stepping


class Simulation:
    def __init__(self, live: Iterable[Cell] = ()) -> None:
        self.live = set(live)
        self.generation = 0
        self.running = False
        self.speed = 10.0  # generations a second
        self.waited = 0.0

    def step(self) -> None:
        self.live = step(self.live)
        self.generation += 1

    def update(self, seconds: float) -> None:
        """Let some time go by, and step as often as that allows, within reason.

        A big universe can take longer to step than a frame lasts. Rather than
        fall further and further behind, we catch up by five generations at the
        most, and stop early if this frame has used up its share of the time.
        """
        if not self.running:
            return
        interval = 1 / self.speed
        self.waited = min(self.waited + seconds, 5 * interval)
        deadline = time.perf_counter() + FRAME_BUDGET
        while self.waited >= interval and time.perf_counter() < deadline:
            self.waited -= interval
            self.step()

    def paint(self, cell: Cell, alive: bool) -> None:
        """Bring one cell to life, or kill it."""
        if alive:
            self.live.add(cell)
        else:
            self.live.discard(cell)

    def load(self, pattern: set[Cell], at: Cell = (0, 0)) -> None:
        """Replace the universe with a pattern, and start counting again."""
        self.live = shift(pattern, *at)
        self.generation = 0

    def faster(self, factor: float) -> None:
        self.speed = max(1.0, min(240.0, self.speed * factor))
