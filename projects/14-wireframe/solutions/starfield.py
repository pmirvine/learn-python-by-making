"""Extend 2: stars that fly past. A few thousand small objects are what slots are for.

To use it, give the View a Starfield, and in View.draw, straight after the fill:

    self.stars.update(seconds)
    self.stars.draw(self.window)

(draw will need to be told how many seconds have gone by.)
"""

import random

import pygame


class Star:
    __slots__ = ("x", "y", "z")

    def __init__(self, rng: random.Random, z: float | None = None) -> None:
        self.x = rng.uniform(-1, 1)
        self.y = rng.uniform(-1, 1)
        self.z = rng.uniform(0.05, 1) if z is None else z


class Starfield:
    def __init__(self, count: int, rng: random.Random, speed: float = 0.25) -> None:
        self.rng = rng
        self.speed = speed
        self.stars = [Star(rng) for _ in range(count)]

    def update(self, seconds: float) -> None:
        for number, star in enumerate(self.stars):
            star.z -= self.speed * seconds
            if star.z <= 0.05:
                self.stars[number] = Star(self.rng, z=1.0)

    def draw(self, window: pygame.Surface) -> None:
        width, height = window.get_size()
        for star in self.stars:
            x = round(width / 2 + star.x / star.z * width / 2)
            y = round(height / 2 - star.y / star.z * height / 2)
            if 0 <= x < width and 0 <= y < height:
                glow = round(255 * (1 - star.z))
                window.set_at((x, y), (glow, glow, glow))
