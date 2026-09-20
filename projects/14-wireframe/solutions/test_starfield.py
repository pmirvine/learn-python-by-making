import random

import pygame
import pytest
from starfield import Star, Starfield


def test_stars_come_towards_you_and_start_again_at_the_back():
    field = Starfield(200, random.Random(14), speed=0.5)
    before = [star.z for star in field.stars]
    field.update(0.1)
    after = [star.z for star in field.stars]
    nearer = [new < old for old, new in zip(before, after, strict=True)]
    assert nearer.count(True) > 150
    assert 1.0 in after
    assert all(0.05 < z <= 1.0 for z in after)


def test_a_slip_of_the_finger_is_an_error():
    star = Star(random.Random(1))
    with pytest.raises(AttributeError):
        star.zed = 0.5


def test_drawing_lights_some_pixels():
    window = pygame.Surface((320, 240))
    Starfield(500, random.Random(14)).draw(window)
    lit = pygame.mask.from_threshold(window, (0, 0, 0), (1, 1, 1))
    lit.invert()
    assert 100 < lit.count() <= 500
