"""Checking a ship for faces that are wound the wrong way round."""

from wireframe.model import Ship
from wireframe.projection import normal
from wireframe.vec3 import Vec3


def inside_out(ship: Ship) -> list[int]:
    """Return the numbers of the faces whose corners run clockwise, seen from outside.

    It's right for any ship that has no dents in it. A face of such a ship points
    away from the middle, so something is wrong with a face that points towards it.
    """
    middle = sum(ship.points, Vec3()) * (1 / len(ship.points))
    wrong = []
    for number, face in enumerate(ship.faces):
        corners = [ship.points[corner] for corner in face.points]
        if normal(corners).dot(corners[0] - middle) < 0:
            wrong.append(number)
    return wrong
