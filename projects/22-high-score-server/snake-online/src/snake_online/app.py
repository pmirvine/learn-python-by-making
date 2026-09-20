"""Project 9's Snake, with four more lines: when a game ends, the score is sent."""

import logging

import httpx
import pygame
from snake.app import FRAME_RATE, WINDOW_SIZE, handle
from snake.model import Game, State
from snake.view import View

from snake_online.scores import ordinal, post_score


class Reporter:
    """Watches a game, and sends its score at the moment that it ends."""

    def __init__(self, client: httpx.Client | None = None) -> None:
        self.client = client
        self.was_over = False
        self.caption = "Snake"

    def watch(self, game: Game) -> None:
        over = game.state is State.GAME_OVER
        if over and not self.was_over:
            row = post_score("snake", game.score, self.client)
            place = f"you came {ordinal(row['rank'])}" if row else "the server is away"
            self.caption = f"Snake: {game.score}, and {place}"
        self.was_over = over


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE, pygame.SCALED | pygame.RESIZABLE)
    clock = pygame.time.Clock()
    game = Game()
    view = View(game, window)
    reporter = Reporter()

    running = True
    while running:
        for event in pygame.event.get():
            running = handle(event, game) and running
        game.update(clock.tick(FRAME_RATE) / 1000)
        reporter.watch(game)
        pygame.display.set_caption(reporter.caption)
        view.draw()
        pygame.display.flip()

    pygame.quit()
