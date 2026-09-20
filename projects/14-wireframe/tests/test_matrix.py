import pytest

from wireframe.matrix import IDENTITY, Matrix, rotation_x, rotation_y, rotation_z
from wireframe.vec3 import Vec3


def numbers(matrix: Matrix) -> list[float]:
    return [number for row in matrix.rows for number in row]


def test_multiplying_by_hand():
    a = Matrix(((1, 2), (3, 4)))
    b = Matrix(((5, 6), (7, 8)))
    assert a @ b == Matrix(((19, 22), (43, 50)))


def test_the_shapes_have_to_fit():
    with pytest.raises(ValueError, match="shorter"):
        Matrix(((1, 2, 3), (4, 5, 6))) @ Matrix(((1, 2), (3, 4)))


def test_columns_and_transposing():
    matrix = Matrix(((1, 2, 3), (4, 5, 6)))
    assert matrix.columns == ((1, 4), (2, 5), (3, 6))
    assert matrix.transposed().transposed() == matrix


def test_the_identity_changes_nothing():
    turn = rotation_y(40)
    assert IDENTITY @ turn == turn
    assert turn @ IDENTITY == turn
    assert IDENTITY @ Vec3(1, 2, 3) == Vec3(1, 2, 3)


@pytest.mark.parametrize(
    ("turn", "start", "end"),
    [
        (rotation_x(90), Vec3(0, 1, 0), Vec3(0, 0, 1)),
        (rotation_y(90), Vec3(0, 0, 1), Vec3(1, 0, 0)),
        (rotation_z(90), Vec3(1, 0, 0), Vec3(0, 1, 0)),
    ],
)
def test_a_quarter_turn(turn, start, end):
    assert tuple(turn @ start) == pytest.approx(tuple(end))


def test_the_order_matters():
    pitch, roll = rotation_x(90), rotation_z(90)
    nose = Vec3(0, 0, 1)
    assert tuple(pitch @ roll @ nose) == pytest.approx((0, -1, 0))
    assert tuple(roll @ pitch @ nose) == pytest.approx((1, 0, 0))


def test_two_turns_in_one_matrix():
    both = rotation_x(30) @ rotation_y(45)
    point = Vec3(3, 4, 5)
    assert tuple(both @ point) == pytest.approx(
        tuple(rotation_x(30) @ (rotation_y(45) @ point))
    )


def test_transposing_a_rotation_undoes_it():
    turn = rotation_x(25) @ rotation_y(-70) @ rotation_z(130)
    assert numbers(turn.transposed() @ turn) == pytest.approx(numbers(IDENTITY))


def test_a_rotation_changes_no_lengths():
    turn = rotation_x(25) @ rotation_y(-70) @ rotation_z(130)
    assert abs(turn @ Vec3(2, 3, 6)) == pytest.approx(7)
