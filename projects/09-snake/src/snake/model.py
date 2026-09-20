"""The game of Snake: its rules and its state. There's no Pygame in here."""

import random
from collections import deque
from enum import Enum, auto

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


class State(Enum):
    TITLE = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()


class Game:
    """One game of Snake: the board, the snake, the food and the score."""

    START_INTERVAL = 0.14
    FASTEST_INTERVAL = 0.05

    def __init__(
        self, columns: int = 32, rows: int = 24, rng: random.Random | None = None
    ) -> None:
        self.columns = columns
        self.rows = rows
        self.rng = rng or random.Random()
        self.state = State.TITLE
        self.best = 0
        self.reset()

    def reset(self) -> None:
        """Set up a new round. The best score is kept."""
        self.snake = Snake((self.columns // 2, self.rows // 2))
        self.score = 0
        self.interval = self.START_INTERVAL
        self.waited = 0.0
        self.food = self.free_cell()

    def free_cell(self) -> Cell:
        """Choose a random cell that the snake isn't on."""
        while True:
            cell = (self.rng.randrange(self.columns), self.rng.randrange(self.rows))
            if cell not in self.snake.body:
                return cell

    def start(self) -> None:
        """Begin a round, from the title screen or after a game over."""
        if self.state in (State.TITLE, State.GAME_OVER):
            self.reset()
            self.state = State.PLAYING

    def toggle_pause(self) -> None:
        if self.state is State.PLAYING:
            self.state = State.PAUSED
        elif self.state is State.PAUSED:
            self.state = State.PLAYING

    def turn(self, direction: Direction) -> None:
        if self.state is State.PLAYING:
            self.snake.turn(direction)

    def update(self, seconds: float) -> None:
        """Let this much time go by. The snake steps whenever enough has built up."""
        if self.state is not State.PLAYING:
            return
        self.waited += seconds
        while self.waited >= self.interval and self.state is State.PLAYING:
            self.waited -= self.interval
            self.step()

    def step(self) -> None:
        """Move the snake on by one cell, and deal with whatever it has run into."""
        self.snake.advance()
        x, y = self.snake.head()
        off_the_board = not (0 <= x < self.columns and 0 <= y < self.rows)
        if off_the_board or self.snake.bites_itself():
            self.state = State.GAME_OVER
            self.best = max(self.best, self.score)
        elif self.snake.head() == self.food:
            self.snake.grow()
            self.score += 10
            self.interval = max(self.FASTEST_INTERVAL, self.interval * 0.96)
            self.food = self.free_cell()
