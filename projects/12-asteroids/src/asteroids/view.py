"""Drawing the game, in white lines on black, as the arcade machine did."""

from typing import Protocol

import pygame

from asteroids.model import Game, State
from asteroids.vector import Vector

WHITE = (255, 255, 255)
GREY = (150, 150, 150)


class Shape(Protocol):
    """Anything that can say what its outline is can be drawn."""

    def outline(self) -> list[Vector]: ...


class View:
    def __init__(self, game: Game, window: pygame.Surface) -> None:
        self.game = game
        self.window = window
        self.big = pygame.font.Font(None, 72)
        self.small = pygame.font.Font(None, 28)

    def polygon(self, shape: Shape, colour: tuple[int, int, int] = WHITE) -> None:
        points = [tuple(point) for point in shape.outline()]
        pygame.draw.polygon(self.window, colour, points, width=1)

    def text(self, font: pygame.font.Font, message: str, y: int) -> None:
        image = font.render(message, True, WHITE)
        x = (self.window.get_width() - image.get_width()) // 2
        self.window.blit(image, (x, y))

    def draw(self) -> None:
        game = self.game
        self.window.fill("black")

        for rock in game.rocks:
            self.polygon(rock, GREY)
        for bullet in game.bullets:
            pygame.draw.circle(self.window, WHITE, tuple(bullet.position), 2)
        if game.state is State.PLAYING:
            self.polygon(game.ship)
            if game.ship.thrusting:
                tail = game.ship.position + Vector.from_polar(-16, game.ship.heading)
                pygame.draw.circle(self.window, WHITE, tuple(tail), 3, width=1)

        status = f"{game.score:05}     SHIPS {game.lives}     WAVE {game.wave}"
        self.window.blit(self.small.render(status, True, WHITE), (16, 12))
        match game.state:
            case State.TITLE:
                self.text(self.big, "ASTEROIDS", 200)
                self.text(self.small, "ARROWS TO TURN AND THRUST, SPACE TO FIRE", 290)
                self.text(self.small, "PRESS ENTER", 330)
            case State.GAME_OVER:
                self.text(self.big, "GAME OVER", 220)
                self.text(self.small, f"BEST {game.best:05}     PRESS ENTER", 300)
