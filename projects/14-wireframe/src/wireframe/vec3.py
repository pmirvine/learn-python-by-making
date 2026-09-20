"""A point, or a direction, in three dimensions."""

import math
from collections.abc import Iterator
from dataclasses import dataclass

from wireframe.matrix import Matrix


@dataclass(frozen=True, slots=True)
class Vec3:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __add__(self, other: "Vec3") -> "Vec3":
        if not isinstance(other, Vec3):
            return NotImplemented
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vec3") -> "Vec3":
        if not isinstance(other, Vec3):
            return NotImplemented
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, number: float) -> "Vec3":
        if not isinstance(number, (int, float)):
            return NotImplemented
        return Vec3(self.x * number, self.y * number, self.z * number)

    def __rmatmul__(self, matrix: Matrix) -> "Vec3":
        """Work out `matrix @ self`: each row times this vector, added up."""
        if not isinstance(matrix, Matrix):
            return NotImplemented
        return Vec3(
            *(sum(a * b for a, b in zip(row, self, strict=True)) for row in matrix.rows)
        )

    def __abs__(self) -> float:
        return math.hypot(self.x, self.y, self.z)

    def __iter__(self) -> Iterator[float]:
        yield self.x
        yield self.y
        yield self.z

    def dot(self, other: "Vec3") -> float:
        """How far two directions agree. It's positive if they point the same way."""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: "Vec3") -> "Vec3":
        """A direction at right angles to both."""
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )
