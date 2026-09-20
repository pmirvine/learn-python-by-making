import pytest

from asteroids.vector import Vector


def test_vectors_with_equal_parts_are_equal():
    assert Vector(3, 4) == Vector(3, 4)
    assert Vector(3, 4) != Vector(4, 3)
    assert Vector() == Vector(0, 0)


def test_vectors_can_be_keys_and_members():
    assert len({Vector(1, 2), Vector(1, 2), Vector(2, 1)}) == 2
    assert {Vector(1, 2): "here"}[Vector(1, 2)] == "here"


def test_vectors_cannot_be_changed():
    with pytest.raises(AttributeError):
        Vector(1, 2).x = 5


def test_adding_and_subtracting():
    assert Vector(1, 2) + Vector(10, 20) == Vector(11, 22)
    assert Vector(10, 20) - Vector(1, 2) == Vector(9, 18)
    assert -Vector(1, -2) == Vector(-1, 2)


def test_adding_leaves_both_vectors_alone():
    a, b = Vector(1, 2), Vector(3, 4)
    total = a + b
    assert (a, b, total) == (Vector(1, 2), Vector(3, 4), Vector(4, 6))


def test_plus_equals_makes_a_new_vector():
    position = start = Vector(1, 1)
    position += Vector(2, 2)
    assert position == Vector(3, 3)
    assert start == Vector(1, 1)


def test_scaling_works_from_either_side():
    assert Vector(1, 2) * 3 == Vector(3, 6)
    assert 3 * Vector(1, 2) == Vector(3, 6)
    assert Vector(3, 6) / 3 == Vector(1, 2)


@pytest.mark.parametrize("nonsense", ["3", None, [1, 2]])
def test_nonsense_is_refused_politely(nonsense):
    with pytest.raises(TypeError, match="unsupported operand"):
        Vector(1, 2) + nonsense
    with pytest.raises(TypeError, match="unsupported operand|can't multiply"):
        Vector(1, 2) * nonsense


def test_length_truth_and_unpacking():
    assert abs(Vector(3, 4)) == 5
    assert Vector(0, 0.001)
    assert not Vector(0, 0)
    x, y = Vector(7, 8)
    assert (x, y) == (7, 8)
    assert tuple(Vector(7, 8)) == (7, 8)


def test_sum_works_given_a_vector_to_start_from():
    forces = [Vector(1, 0), Vector(0, 2), Vector(-3, 1)]
    assert sum(forces, Vector()) == Vector(-2, 3)


@pytest.mark.parametrize(
    ("degrees", "expected"),
    [(0, (0, -10)), (90, (10, 0)), (180, (0, 10)), (270, (-10, 0))],
)
def test_from_polar_measures_clockwise_from_straight_up(degrees, expected):
    assert tuple(Vector.from_polar(10, degrees)) == pytest.approx(expected, abs=1e-9)


def test_rotation_is_clockwise_and_keeps_the_length():
    turned = Vector(0, -5).rotated(90)
    assert tuple(turned) == pytest.approx((5, 0), abs=1e-9)
    assert abs(Vector(3, 4).rotated(37)) == pytest.approx(5)


def test_wrapping_brings_a_point_back_onto_the_screen():
    assert Vector(810, -5).wrapped(800, 600) == Vector(10, 595)
    assert Vector(400, 300).wrapped(800, 600) == Vector(400, 300)


def test_a_vector_describes_itself():
    assert repr(Vector(1.5, -2)) == "Vector(x=1.5, y=-2)"
