import pygame

from breakout.app import steering
from breakout.model import Game, Level, State
from breakout.view import View


def test_every_state_can_be_drawn():
    pygame.init()
    window = pygame.display.set_mode((640, 512))
    game = Game(levels=[Level.from_text("RYG#")])
    view = View(game, window)
    for state in State:
        game.state = state
        view.draw()
    brick = game.level.bricks[0].rect
    assert view.canvas.get_at((int(brick.centerx), int(brick.centery)))[:3] == (
        255,
        0,
        0,
    )


def test_steering():
    keys = {pygame.K_LEFT: False, pygame.K_RIGHT: True}
    assert steering(keys) == 1
    assert steering({pygame.K_LEFT: True, pygame.K_RIGHT: True}) == 0
    assert steering({pygame.K_LEFT: True, pygame.K_RIGHT: False}) == -1
