import random

import pygame

from snake.app import handle
from snake.model import Direction, Game, State
from snake.view import CELL, GREEN, RED, YELLOW, View


def test_the_view_draws_the_snake_and_the_food():
    pygame.init()
    window = pygame.display.set_mode((320, 240))
    game = Game(columns=20, rows=15, rng=random.Random(2))
    view = View(game, window)
    view.draw()

    hx, hy = game.snake.head()
    fx, fy = game.food
    assert view.canvas.get_at((hx * CELL + 2, hy * CELL + 2))[:3] == YELLOW
    assert view.canvas.get_at(((hx - 1) * CELL + 2, hy * CELL + 2))[:3] == GREEN
    assert view.canvas.get_at((fx * CELL + 2, fy * CELL + 2))[:3] == RED


def test_every_state_can_be_drawn():
    pygame.init()
    window = pygame.display.set_mode((320, 240))
    game = Game()
    view = View(game, window)
    for state in State:
        game.state = state
        view.draw()


def key(code: int) -> pygame.event.Event:
    return pygame.event.Event(pygame.KEYDOWN, key=code)


def test_keys_drive_the_game():
    game = Game()
    assert handle(key(pygame.K_SPACE), game)
    assert game.state is State.PLAYING
    assert handle(key(pygame.K_UP), game)
    assert list(game.snake.turns) == [Direction.UP]
    assert handle(key(pygame.K_p), game)
    assert game.state is State.PAUSED


def test_escape_and_the_close_button_stop_the_program():
    game = Game()
    assert not handle(key(pygame.K_ESCAPE), game)
    assert not handle(pygame.event.Event(pygame.QUIT), game)
