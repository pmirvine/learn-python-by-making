"""A two-dimensional vector that works with Python's own operators."""

import math
from collections.abc import Iterator
from dataclasses import dataclass


@dataclass(frozen=True)
class Vector:
    """A direction and a length, or a point. It can't be changed once it's made."""

    x: float = 0.0
    y: float = 0.0

    @classmethod
    def from_polar(cls, length: float, degrees: float) -> "Vector":
        """Make a vector from its length, and its angle clockwise from straight up."""
        angle = math.radians(degrees)
        return cls(length * math.sin(angle), -length * math.cos(angle))

    def __add__(self, other: "Vector") -> "Vector":
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scale: float) -> "Vector":
        if not isinstance(scale, (int, float)):
            return NotImplemented
        return Vector(self.x * scale, self.y * scale)

    def __rmul__(self, scale: float) -> "Vector":
        return self * scale

    def __truediv__(self, scale: float) -> "Vector":
        if not isinstance(scale, (int, float)):
            return NotImplemented
        return Vector(self.x / scale, self.y / scale)

    def __neg__(self) -> "Vector":
        return Vector(-self.x, -self.y)

    def __abs__(self) -> float:
        return math.hypot(self.x, self.y)

    def __bool__(self) -> bool:
        return self.x != 0 or self.y != 0

    def __iter__(self) -> Iterator[float]:
        yield self.x
        yield self.y

    def rotated(self, degrees: float) -> "Vector":
        """Return this vector, turned clockwise by some degrees."""
        angle = math.radians(degrees)
        cos, sin = math.cos(angle), math.sin(angle)
        return Vector(self.x * cos - self.y * sin, self.x * sin + self.y * cos)

    def wrapped(self, width: float, height: float) -> "Vector":
        """Return this point, brought back onto a screen that wraps round."""
        return Vector(self.x % width, self.y % height)
