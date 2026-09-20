"""The program: a window, a loop, and the keyboard."""

import pygame

from breakout.model import Game
from breakout.view import View

WINDOW_SIZE = (960, 768)
FRAME_RATE = 60


def steering(pressed: pygame.key.ScancodeWrapper) -> int:
    """Which way the player is steering: -1 for left, 1 for right, 0 for neither or both."""
    return int(pressed[pygame.K_RIGHT]) - int(pressed[pygame.K_LEFT])


def main() -> None:
    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE, pygame.SCALED | pygame.RESIZABLE)
    pygame.display.set_caption("Breakout")
    clock = pygame.time.Clock()

    game = Game()
    view = View(game, window)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    game.serve()

        seconds = clock.tick(FRAME_RATE) / 1000
        game.update(seconds, steering(pygame.key.get_pressed()))

        view.draw()
        pygame.display.flip()

    pygame.quit()
