import pytest

from wireframe.projection import brightness, faces_the_eye, normal, project
from wireframe.vec3 import Vec3

CENTRE = (160, 120)
# A triangle in the plane z = 0, anticlockwise as seen from the +z side.
TOWARDS = [Vec3(0, 0, 0), Vec3(1, 0, 0), Vec3(0, 1, 0)]
AWAY = list(reversed(TOWARDS))


def test_the_middle_of_the_world_is_the_middle_of_the_screen():
    assert project(Vec3(0, 0, 0), 100, 240, CENTRE) == CENTRE


def test_y_goes_up_in_the_world_and_down_on_the_screen():
    assert project(Vec3(10, 10, 0), 100, 240, CENTRE) == (184, 96)


def test_nearer_things_look_bigger():
    near = project(Vec3(10, 0, 50), 100, 240, CENTRE)
    far = project(Vec3(10, 0, -50), 100, 240, CENTRE)
    assert near == (208, 120)
    assert far == (176, 120)


def test_anticlockwise_corners_face_outwards():
    assert normal(TOWARDS) == Vec3(0, 0, 1)
    assert normal(AWAY) == Vec3(0, 0, -1)


def test_which_faces_face_the_eye():
    assert faces_the_eye(TOWARDS, 100)
    assert not faces_the_eye(AWAY, 100)


def test_perspective_matters_to_what_you_can_see():
    # The side of a box, facing right. From dead ahead it would be edge-on, but
    # it's off to the left, and so the eye can see it.
    side = [Vec3(-30, 0, 0), Vec3(-30, 0, -10), Vec3(-30, 10, -10)]
    assert normal(side).x > 0
    assert normal(side).z == 0
    assert faces_the_eye(side, 100)


def test_brightness():
    assert brightness(TOWARDS) == pytest.approx(3 / 14**0.5)
    assert brightness(AWAY) == 0
