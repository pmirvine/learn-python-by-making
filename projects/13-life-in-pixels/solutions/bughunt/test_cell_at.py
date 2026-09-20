"""The test to hand to `git bisect run`. Copy it into the practice repository.

It calls cell_at with positional arguments only, because the names of the
parameters change during the history, and a test for bisecting has to work at
every commit along the way.
"""

import pytest

camera = pytest.importorskip("camera", reason="run this inside bisect-practice")


def test_cells_left_of_and_above_the_origin():
    assert camera.cell_at(4, 4, -3, -2) == (-3, -2)


def test_cells_below_and_right_of_the_origin_always_worked():
    assert camera.cell_at(20, 12, 3, 2) == (5, 3)
