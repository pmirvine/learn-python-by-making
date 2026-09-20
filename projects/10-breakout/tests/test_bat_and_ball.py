import math

import pytest

from breakout.model import Ball, Bat, Settings


def test_a_bat_starts_in_the_middle_near_the_bottom():
    bat = Bat(Settings())
    assert bat.rect.centerx == 160
    assert bat.rect.bottom == 244


def test_a_bat_moves_at_its_speed():
    bat = Bat(Settings(bat_speed=100))
    bat.move(1, 0.5)
    assert bat.rect.centerx == 210
    bat.move(-1, 0.25)
    assert bat.rect.centerx == 185


def test_a_bat_stops_at_the_walls():
    bat = Bat(Settings())
    bat.move(-1, 10)
    assert bat.rect.left == 0
    bat.move(1, 10)
    assert bat.rect.right == 320


def test_a_new_ball_goes_straight_up():
    ball = Ball(size=5, speed=150)
    assert (ball.vx, ball.vy) == (0, -150)
    assert ball.speed == 150


def test_speed_is_worked_out_from_the_velocity():
    ball = Ball(5, 100)
    ball.vx, ball.vy = 30, -40
    assert ball.speed == 50


def test_setting_the_speed_keeps_the_direction():
    ball = Ball(5, 100)
    ball.vx, ball.vy = 30, -40
    ball.speed = 100
    assert (ball.vx, ball.vy) == pytest.approx((60, -80))


@pytest.mark.parametrize("bad", [0, -1])
def test_a_ball_cannot_stand_still_or_go_backwards(bad):
    ball = Ball(5, 100)
    with pytest.raises(ValueError, match="more than zero"):
        ball.speed = bad


@pytest.mark.parametrize(
    ("offset", "degrees"),
    [(0, 0), (1, 60), (-1, -60), (0.5, 30), (5, 60)],
)
def test_aim_sets_the_angle_and_keeps_the_speed(offset, degrees):
    ball = Ball(5, 200)
    ball.aim(offset)
    assert ball.speed == pytest.approx(200)
    assert math.degrees(math.atan2(ball.vx, -ball.vy)) == pytest.approx(degrees)


def test_things_describe_themselves():
    assert repr(Bat(Settings())) == "Bat(centre=160)"
    assert repr(Ball(5, 150)) == "Ball(at=(2, 2), velocity=(0, -150))"
