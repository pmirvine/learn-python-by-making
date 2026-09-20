"""Extend 2: a flying saucer. It needs no changes to touching() or to the View.

A Saucer has a position and a radius, so it's a Body, and touching() accepts it.
It has an outline(), so it's a Shape, and View.polygon() can draw it. It never
says so, and it inherits from nothing. It simply has what's asked for.
"""

import random

from asteroids.model import HEIGHT, WIDTH
from asteroids.vector import Vector


class Saucer:
    SPEED = 90.0
    OUTLINE = (
        Vector(-18, 0),
        Vector(-8, -7),
        Vector(-4, -13),
        Vector(4, -13),
        Vector(8, -7),
        Vector(18, 0),
        Vector(8, 7),
        Vector(-8, 7),
    )

    def __init__(self, rng: random.Random) -> None:
        self.rng = rng
        self.position = Vector(0, rng.uniform(60, HEIGHT - 60))
        self.velocity = Vector(self.SPEED, 0)
        self.radius = 16.0
        self.until_swerve = 1.0

    def update(self, seconds: float) -> None:
        self.until_swerve -= seconds
        if self.until_swerve <= 0:
            self.velocity = Vector(self.SPEED, self.rng.choice([-60, 0, 60]))
            self.until_swerve = self.rng.uniform(0.5, 1.5)
        self.position = (self.position + self.velocity * seconds).wrapped(WIDTH, HEIGHT)

    def outline(self) -> list[Vector]:
        return [self.position + point for point in self.OUTLINE]
