"""Matrices, and the ones that turn things round."""

import math
from dataclasses import dataclass

type Row = tuple[float, ...]


@dataclass(frozen=True, slots=True)
class Matrix:
    rows: tuple[Row, ...]

    @property
    def columns(self) -> tuple[Row, ...]:
        return tuple(zip(*self.rows, strict=True))

    def __matmul__(self, other: "Matrix") -> "Matrix":
        if not isinstance(other, Matrix):
            return NotImplemented
        return Matrix(
            tuple(
                tuple(
                    sum(a * b for a, b in zip(row, column, strict=True))
                    for column in other.columns
                )
                for row in self.rows
            )
        )

    def transposed(self) -> "Matrix":
        """Swap the rows with the columns. For a rotation, that's the way back."""
        return Matrix(self.columns)


IDENTITY = Matrix(((1, 0, 0), (0, 1, 0), (0, 0, 1)))


def rotation_x(degrees: float) -> Matrix:
    """Turn about the x axis: the nose pitches up or down."""
    c, s = math.cos(math.radians(degrees)), math.sin(math.radians(degrees))
    return Matrix(((1, 0, 0), (0, c, -s), (0, s, c)))


def rotation_y(degrees: float) -> Matrix:
    """Turn about the y axis: the nose yaws to the left or the right."""
    c, s = math.cos(math.radians(degrees)), math.sin(math.radians(degrees))
    return Matrix(((c, 0, s), (0, 1, 0), (-s, 0, c)))


def rotation_z(degrees: float) -> Matrix:
    """Turn about the z axis: the ship rolls."""
    c, s = math.cos(math.radians(degrees)), math.sin(math.radians(degrees))
    return Matrix(((c, -s, 0), (s, c, 0), (0, 0, 1)))
