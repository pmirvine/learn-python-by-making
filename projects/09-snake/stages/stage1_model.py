"""The game of Snake: its rules and its state. There's no Pygame in here."""

from collections import deque
from enum import Enum

type Cell = tuple[int, int]


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def opposite(self) -> "Direction":
        dx, dy = self.value
        return Direction((-dx, -dy))


class Snake:
    """A snake on a grid: a body of cells, head first, and a heading."""

    START_LENGTH = 4

    def __init__(self, head: Cell, heading: Direction = Direction.RIGHT) -> None:
        x, y = head
        dx, dy = heading.value
        self.body = deque((x - n * dx, y - n * dy) for n in range(self.START_LENGTH))
        self.heading = heading
        self.turns: deque[Direction] = deque(maxlen=2)
        self.growing = 0

    def head(self) -> Cell:
        return self.body[0]

    def turn(self, direction: Direction) -> None:
        """Ask to turn at the next step. A snake can't turn back on itself."""
        latest = self.turns[-1] if self.turns else self.heading
        if direction not in (latest, latest.opposite()):
            self.turns.append(direction)

    def grow(self, cells: int = 1) -> None:
        """Get longer by this many cells, over the next few steps."""
        self.growing += cells

    def advance(self) -> None:
        """Move one cell forward, taking the next turn that's waiting, if any."""
        if self.turns:
            self.heading = self.turns.popleft()
        x, y = self.head()
        dx, dy = self.heading.value
        self.body.appendleft((x + dx, y + dy))
        if self.growing:
            self.growing -= 1
        else:
            self.body.pop()

    def bites_itself(self) -> bool:
        return self.body.count(self.head()) > 1
