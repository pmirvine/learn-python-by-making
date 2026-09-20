import random

import pygame

from asteroids.app import SOUNDS, controls
from asteroids.model import Controls, Game, State
from asteroids.view import View


def test_every_state_can_be_drawn():
    pygame.init()
    window = pygame.display.set_mode((800, 600))
    game = Game(random.Random(3))
    view = View(game, window)
    game.ship.thrusting = True
    for state in State:
        game.state = state
        view.draw()

    game.state = State.PLAYING
    view.draw()
    nose = (400, 286)
    assert window.get_at(nose)[:3] == (255, 255, 255)


def test_held_keys_become_controls():
    keys = {
        pygame.K_LEFT: True,
        pygame.K_RIGHT: False,
        pygame.K_UP: True,
        pygame.K_SPACE: False,
    }
    assert controls(keys) == Controls(turn=-1, thrust=True, fire=False)


def test_every_event_has_a_sound():
    game = Game(random.Random(3))
    game.start()
    game.update(0.01, Controls(fire=True))
    assert set(game.events) <= set(SOUNDS)
    assert set(SOUNDS) == {"fire", "bang", "crash"}
