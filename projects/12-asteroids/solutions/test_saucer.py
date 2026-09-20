import random

from saucer import Saucer

from asteroids.model import Bullet, Zone, touching
from asteroids.vector import Vector


def test_a_saucer_is_a_body_without_ever_saying_so():
    saucer = Saucer(random.Random(1))
    assert touching(saucer, Bullet(saucer.position + Vector(10, 0), Vector()))
    assert not touching(saucer, Zone(saucer.position + Vector(100, 0), 5))


def test_a_saucer_is_a_shape_without_ever_saying_so():
    saucer = Saucer(random.Random(1))
    outline = saucer.outline()
    assert len(outline) == 8
    assert all(abs(point - saucer.position) <= 18 for point in outline)


def test_a_saucer_crosses_the_screen_and_swerves():
    saucer = Saucer(random.Random(1))
    heights = set()
    for _ in range(600):
        saucer.update(1 / 60)
        heights.add(round(saucer.velocity.y))
    assert saucer.position.x > 0
    assert len(heights) > 1
