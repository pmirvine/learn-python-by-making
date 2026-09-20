from wireframe.vec3 import Vec3


def test_arithmetic():
    assert Vec3(1, 2, 3) + Vec3(10, 20, 30) == Vec3(11, 22, 33)
    assert Vec3(11, 22, 33) - Vec3(10, 20, 30) == Vec3(1, 2, 3)
    assert Vec3(1, 2, 3) * 2 == Vec3(2, 4, 6)


def test_length_and_unpacking():
    assert abs(Vec3(2, 3, 6)) == 7
    x, y, z = Vec3(1, 2, 3)
    assert (x, y, z) == (1, 2, 3)


def test_dot_says_how_far_two_directions_agree():
    assert Vec3(1, 0, 0).dot(Vec3(5, 0, 0)) > 0
    assert Vec3(1, 0, 0).dot(Vec3(0, 7, 0)) == 0
    assert Vec3(1, 0, 0).dot(Vec3(-2, 1, 1)) < 0


def test_cross_is_at_right_angles_to_both():
    a, b = Vec3(1, 2, 3), Vec3(-4, 0, 5)
    assert a.cross(b).dot(a) == 0
    assert a.cross(b).dot(b) == 0
    assert Vec3(1, 0, 0).cross(Vec3(0, 1, 0)) == Vec3(0, 0, 1)


def test_there_is_nowhere_to_put_anything_else():
    assert not hasattr(Vec3(1, 2, 3), "__dict__")
