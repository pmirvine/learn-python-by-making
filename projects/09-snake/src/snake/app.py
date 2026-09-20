"""The program: a window, a loop, and the keyboard."""

import pygame

from snake.model import Direction, Game
from snake.view import View

WINDOW_SIZE = (768, 576)
FRAME_RATE = 60

KEYS = {
    pygame.K_UP: Direction.UP,
    pygame.K_DOWN: Direction.DOWN,
    pygame.K_LEFT: Direction.LEFT,
    pygame.K_RIGHT: Direction.RIGHT,
}


def handle(event: pygame.event.Event, game: Game) -> bool:
    """Pass an event on to the game. Return False if it's time to stop."""
    if event.type == pygame.QUIT:
        return False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return False
        if event.key == pygame.K_SPACE:
            game.start()
        elif event.key == pygame.K_p:
            game.toggle_pause()
        elif event.key in KEYS:
            game.turn(KEYS[event.key])
    return True


def main() -> None:
    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE, pygame.SCALED | pygame.RESIZABLE)
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    game = Game()
    view = View(game, window)

    running = True
    while running:
        for event in pygame.event.get():
            running = handle(event, game) and running

        seconds = clock.tick(FRAME_RATE) / 1000
        game.update(seconds)

        view.draw()
        pygame.display.flip()

    pygame.quit()
