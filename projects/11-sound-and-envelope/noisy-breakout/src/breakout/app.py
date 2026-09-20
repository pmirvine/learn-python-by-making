"""The program: a window, a loop, and the keyboard."""

import beeb
import pygame

from breakout.model import Game
from breakout.view import View

WINDOW_SIZE = (960, 768)
FRAME_RATE = 60

# For each thing that can happen: a channel, an amplitude or envelope, a pitch and a duration.
SOUNDS = {
    "wall": (1, -7, 101, 1),
    "bat": (1, -12, 53, 2),
    "brick": (2, -12, 149, 1),
    "lost": (3, 1, 5, 14),
    "cleared": (3, 2, 101, 12),
}


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
    beeb.envelope(1, decay=0.7, sustain=0.0)
    beeb.envelope(2, attack=0.05, decay=0.2, sustain=0.5, release=0.4)

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
        for event in game.events:
            beeb.sound(*SOUNDS[event])
        game.events.clear()

        view.draw()
        pygame.display.flip()

    pygame.quit()
