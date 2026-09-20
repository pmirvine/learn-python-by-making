"""The game of Asteroids: its rules and its state. There's no Pygame in here."""

import random
from dataclasses import dataclass
from typing import Protocol

from asteroids.vector import Vector

WIDTH, HEIGHT = 800, 600


@dataclass
class Controls:
    """What the player is asking for, at this moment."""

    turn: int = 0  # -1 for left, 1 for right
    thrust: bool = False
    fire: bool = False


class Body(Protocol):
    """Anything that has a place and a size, and so can hit things."""

    position: Vector
    radius: float


def touching(a: Body, b: Body) -> bool:
    """Are two bodies overlapping? Each of them is treated as a circle."""
    return abs(a.position - b.position) < a.radius + b.radius


@dataclass
class Zone:
    """A circle with nothing in it. It's a Body, because it has what a Body has."""

    position: Vector
    radius: float


class Ship:
    TURN_SPEED = 240.0  # degrees a second
    THRUST = 260.0  # pixels a second, every second
    DRAG = 0.4  # the fraction of its speed that it loses every second
    RELOAD = 0.22  # seconds between shots
    OUTLINE = (Vector(0, -14), Vector(10, 12), Vector(0, 6), Vector(-10, 12))

    def __init__(self, position: Vector) -> None:
        self.position = position
        self.velocity = Vector()
        self.heading = 0.0  # degrees clockwise from straight up
        self.radius = 10.0
        self.reloading = 0.0
        self.thrusting = False

    def update(self, seconds: float, controls: Controls) -> None:
        self.heading = (self.heading + controls.turn * self.TURN_SPEED * seconds) % 360
        self.thrusting = controls.thrust
        if controls.thrust:
            self.velocity += Vector.from_polar(self.THRUST * seconds, self.heading)
        self.velocity *= 1 - self.DRAG * seconds
        self.position = (self.position + self.velocity * seconds).wrapped(WIDTH, HEIGHT)
        self.reloading = max(0.0, self.reloading - seconds)

    def fire(self) -> "Bullet | None":
        """Return a new bullet, leaving from the nose, or None if the gun isn't ready."""
        if self.reloading > 0:
            return None
        self.reloading = self.RELOAD
        nose = self.position + Vector.from_polar(14, self.heading)
        return Bullet(
            nose, self.velocity + Vector.from_polar(Bullet.SPEED, self.heading)
        )

    def outline(self) -> list[Vector]:
        return [self.position + point.rotated(self.heading) for point in self.OUTLINE]

    def __repr__(self) -> str:
        return f"Ship(at={self.position}, heading={self.heading:.0f})"


class Bullet:
    SPEED = 420.0
    LIFETIME = 1.1

    def __init__(self, position: Vector, velocity: Vector) -> None:
        self.position = position
        self.velocity = velocity
        self.radius = 1.5
        self.age = 0.0

    def update(self, seconds: float) -> None:
        self.position = (self.position + self.velocity * seconds).wrapped(WIDTH, HEIGHT)
        self.age += seconds

    @property
    def spent(self) -> bool:
        return self.age >= self.LIFETIME


# For each size of rock, from big to small: how big it is, and what it's worth.
ROCK_RADII = {3: 40.0, 2: 22.0, 1: 11.0}
ROCK_POINTS = {3: 20, 2: 50, 1: 100}


class Rock:
    def __init__(
        self, position: Vector, velocity: Vector, size: int, rng: random.Random
    ) -> None:
        self.position = position
        self.velocity = velocity
        self.size = size
        self.radius = ROCK_RADII[size]
        self.spin = rng.uniform(-90, 90)
        self.angle = 0.0
        # A lumpy outline: a dozen points round a circle, each pushed in or out a bit.
        self.shape = [
            Vector.from_polar(self.radius * rng.uniform(0.75, 1.2), degrees)
            for degrees in range(0, 360, 30)
        ]

    def update(self, seconds: float) -> None:
        self.position = (self.position + self.velocity * seconds).wrapped(WIDTH, HEIGHT)
        self.angle = (self.angle + self.spin * seconds) % 360

    def split(self, rng: random.Random) -> list["Rock"]:
        """Return the two smaller rocks that this one breaks into, or none at all."""
        if self.size == 1:
            return []
        return [
            Rock(self.position, self.velocity.rotated(turn) * 1.4, self.size - 1, rng)
            for turn in (rng.uniform(20, 70), rng.uniform(-70, -20))
        ]

    def outline(self) -> list[Vector]:
        return [self.position + point.rotated(self.angle) for point in self.shape]

    def __repr__(self) -> str:
        return f"Rock(size={self.size}, at={self.position})"
