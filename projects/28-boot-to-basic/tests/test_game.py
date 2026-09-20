"""The type-in game, played by a test: fire all the time, and sooner or later it scores."""

import pygame
from conftest import lines

from micro.computer import Micro


def test_the_carpet(micro: Micro):
    micro.type_in('LOAD "carpet"\nRUN\n')
    while micro.running:
        micro.frame()
    assert lines(micro) == [">"]


def test_alien_can_be_played_and_lost(micro: Micro):
    micro.type_in('LOAD "alien"\nRUN\n')
    micro.press(pygame.K_RETURN)  # hold the fire button down, until something is hit...
    for _ in range(3000):
        micro.frame()
        if micro.machine.variables.get("S", 0.0) >= 10:
            break
    else:
        raise AssertionError("the bolt never hit the alien")

    micro.release(pygame.K_RETURN)  # ...and then stand and wait for the end
    for _ in range(6000):
        if not micro.running:
            break
        micro.frame()
    assert not micro.running, "the alien never reached the bottom"
    assert "GAME OVER" in "".join(lines(micro))
