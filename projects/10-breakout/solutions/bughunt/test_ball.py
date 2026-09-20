"""The failing tests that pin the ball's bug down. Try them on bughunt/ball.py."""

import pytest
from ball import Ball


def test_a_ball_can_be_made():
    assert Ball(speed=200).speed == 200


def test_speed_can_be_changed_and_is_capped():
    ball = Ball(speed=200)
    ball.speed *= 1.05
    assert ball.speed == pytest.approx(210)
    ball.speed = 5000
    assert ball.speed == 900


def test_speed_must_be_positive():
    with pytest.raises(ValueError, match="more than zero"):
        Ball(speed=0)
