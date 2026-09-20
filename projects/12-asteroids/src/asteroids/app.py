"""The program: a window, a loop, the keyboard and the loudspeaker."""

import beeb
import pygame

from asteroids.model import HEIGHT, WIDTH, Controls, Game
from asteroids.view import View

FRAME_RATE = 60

# For each thing that can happen: a channel, an envelope, a pitch and a duration.
SOUNDS = {
    "fire": (1, 1, 180, 3),
    "bang": (0, 2, 0, 8),
    "crash": (0, 3, 0, 30),
}


def controls(pressed: pygame.key.ScancodeWrapper) -> Controls:
    """Read the keys that are being held down."""
    return Controls(
        turn=int(pressed[pygame.K_RIGHT]) - int(pressed[pygame.K_LEFT]),
        thrust=bool(pressed[pygame.K_UP]),
        fire=bool(pressed[pygame.K_SPACE]),
    )


def main() -> None:
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()

    game = Game()
    view = View(game, window)
    beeb.envelope(1, decay=0.12, sustain=0.0)
    beeb.envelope(2, decay=0.4, sustain=0.0)
    beeb.envelope(3, attack=0.02, decay=1.4, sustain=0.0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN:
                    game.start()

        seconds = min(clock.tick(FRAME_RATE) / 1000, 1 / 20)
        game.update(seconds, controls(pygame.key.get_pressed()))
        for event in game.events:
            beeb.sound(*SOUNDS[event])
        game.events.clear()

        view.draw()
        pygame.display.flip()

    pygame.quit()
