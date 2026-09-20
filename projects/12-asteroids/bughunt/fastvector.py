"""A 'faster' vector, which changes itself in place. Every shot makes the ship go faster. Why?"""

import math


class Vector:
    """Like the real one, but it can be changed, and += changes it where it stands."""

    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self.x = x
        self.y = y

    @classmethod
    def from_polar(cls, length: float, degrees: float) -> "Vector":
        angle = math.radians(degrees)
        return cls(length * math.sin(angle), -length * math.cos(angle))

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: "Vector") -> "Vector":
        self.x += other.x
        self.y += other.y
        return self

    def __mul__(self, scale: float) -> "Vector":
        return Vector(self.x * scale, self.y * scale)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Vector) and (self.x, self.y) == (other.x, other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"Vector({self.x:.0f}, {self.y:.0f})"


class Bullet:
    SPEED = 420.0

    def __init__(self, position: Vector, velocity: Vector) -> None:
        self.position = position
        self.velocity = velocity

    def update(self, seconds: float) -> None:
        self.position += self.velocity * seconds


class Ship:
    def __init__(self, position: Vector) -> None:
        self.position = position
        self.velocity = Vector()
        self.heading = 90.0

    def fire(self) -> Bullet:
        velocity = self.velocity
        velocity += Vector.from_polar(Bullet.SPEED, self.heading)
        return Bullet(self.position, velocity)


def main() -> None:
    ship = Ship(Vector(400, 300))
    print(f"Before firing: the ship is at {ship.position}, doing {ship.velocity}")
    for shot in range(1, 4):
        bullet = ship.fire()
        bullet.update(0.5)
        print(
            f"After shot {shot}:  the ship is at {ship.position}, doing {ship.velocity}"
        )


if __name__ == "__main__":
    main()
