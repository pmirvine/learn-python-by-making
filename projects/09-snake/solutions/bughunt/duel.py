"""Light cycles: two snakes that never stop growing. Don't hit anything.

Player one steers with the arrow keys, and player two with W, A, S and D.
The steering is fixed: every cycle has a queue of turns of its own.
"""

from collections import deque
from enum import Enum

import pygame

CELL = 8
COLUMNS, ROWS = 96, 72


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def opposite(self) -> "Direction":
        dx, dy = self.value
        return Direction((-dx, -dy))


class Cycle:
    """A light cycle: it leaves a wall behind it wherever it goes."""

    def __init__(self, start: tuple[int, int], heading: Direction, colour: str) -> None:
        # Made here, in __init__, so that each cycle gets a new one. At class
        # level there would be one deque, shared by every cycle there ever was.
        self.turns: deque[Direction] = deque(maxlen=2)
        self.trail = [start]
        self.heading = heading
        self.colour = colour

    def turn(self, direction: Direction) -> None:
        latest = self.turns[-1] if self.turns else self.heading
        if direction not in (latest, latest.opposite()):
            self.turns.append(direction)

    def advance(self) -> None:
        if self.turns:
            self.heading = self.turns.popleft()
        x, y = self.trail[-1]
        dx, dy = self.heading.value
        self.trail.append((x + dx, y + dy))


PLAYER_ONE = {
    pygame.K_UP: Direction.UP,
    pygame.K_DOWN: Direction.DOWN,
    pygame.K_LEFT: Direction.LEFT,
    pygame.K_RIGHT: Direction.RIGHT,
}
PLAYER_TWO = {
    pygame.K_w: Direction.UP,
    pygame.K_s: Direction.DOWN,
    pygame.K_a: Direction.LEFT,
    pygame.K_d: Direction.RIGHT,
}


def crashed(cycle: Cycle, other: Cycle) -> bool:
    x, y = cycle.trail[-1]
    outside = not (0 <= x < COLUMNS and 0 <= y < ROWS)
    return (
        outside or cycle.trail[-1] in cycle.trail[:-1] or cycle.trail[-1] in other.trail
    )


def main() -> None:
    pygame.init()
    window = pygame.display.set_mode((COLUMNS * CELL, ROWS * CELL))
    pygame.display.set_caption("Light cycles")
    clock = pygame.time.Clock()

    one = Cycle((24, 36), Direction.RIGHT, "yellow")
    two = Cycle((72, 36), Direction.LEFT, "cyan")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key in PLAYER_ONE:
                    one.turn(PLAYER_ONE[event.key])
                if event.key in PLAYER_TWO:
                    two.turn(PLAYER_TWO[event.key])

        one.advance()
        two.advance()
        if crashed(one, two) or crashed(two, one):
            return

        window.fill("black")
        for cycle in (one, two):
            for x, y in cycle.trail:
                pygame.draw.rect(window, cycle.colour, (x * CELL, y * CELL, CELL, CELL))
        pygame.display.flip()
        clock.tick(20)


if __name__ == "__main__":
    main()
    pygame.quit()
