"""Drawing the game. This is the only module that knows what anything looks like."""

import pygame

from snake.model import Cell, Game, State

type Colour = tuple[int, int, int]

CELL = 8  # each cell of the board is this many pixels square, before scaling

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)


class View:
    """Draws a Game onto a small canvas, and scales it up to fill the window."""

    def __init__(self, game: Game, window: pygame.Surface) -> None:
        self.game = game
        self.window = window
        self.canvas = pygame.Surface((game.columns * CELL, game.rows * CELL))
        self.font = pygame.font.Font(None, 16)

    def block(self, cell: Cell, colour: Colour) -> None:
        x, y = cell
        pygame.draw.rect(self.canvas, colour, (x * CELL, y * CELL, CELL - 1, CELL - 1))

    def text(self, message: str, row: int, colour: Colour = WHITE) -> None:
        """Write a line of text, centred, with its top at the given row of cells."""
        image = self.font.render(message, False, colour)
        x = (self.canvas.get_width() - image.get_width()) // 2
        self.canvas.blit(image, (x, row * CELL))

    def draw(self) -> None:
        game = self.game
        self.canvas.fill(BLACK)

        self.block(game.food, RED)
        for cell in game.snake.body:
            self.block(cell, GREEN)
        self.block(game.snake.head(), YELLOW)

        self.text(f"SCORE {game.score:04}   BEST {game.best:04}", 0, CYAN)
        match game.state:
            case State.TITLE:
                self.text("S N A K E", 8, YELLOW)
                self.text("ARROWS TO STEER, P TO PAUSE", 12)
                self.text("PRESS SPACE", 15)
            case State.PAUSED:
                self.text("PAUSED", 10, YELLOW)
            case State.GAME_OVER:
                self.text("GAME OVER", 9, RED)
                self.text("PRESS SPACE", 13)

        scaled = pygame.transform.scale(self.canvas, self.window.get_size())
        self.window.blit(scaled, (0, 0))
