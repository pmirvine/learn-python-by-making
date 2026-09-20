"""From three dimensions to two: where things appear, and which way they face."""

from collections.abc import Sequence

from wireframe.vec3 import Vec3

type Pixel = tuple[int, int]

LIGHT = Vec3(-1, 2, 3)  # the way to the lamp: up, to the left, and behind the eye


def project(point: Vec3, distance: float, scale: float, centre: Pixel) -> Pixel:
    """Return where a point appears, to an eye that's `distance` along the z axis."""
    size = scale / (distance - point.z)
    return round(centre[0] + point.x * size), round(centre[1] - point.y * size)


def normal(corners: Sequence[Vec3]) -> Vec3:
    """Return the way a face points: outwards, if its corners run anticlockwise."""
    a, b, c, *_ = corners
    return (b - a).cross(c - a)


def faces_the_eye(corners: Sequence[Vec3], distance: float) -> bool:
    eye = Vec3(0, 0, distance)
    return normal(corners).dot(eye - corners[0]) > 0


def brightness(corners: Sequence[Vec3]) -> float:
    """Return how well lit a face is, from 0 to 1."""
    outwards = normal(corners)
    return max(0.0, outwards.dot(LIGHT) / (abs(outwards) * abs(LIGHT)))
