"""The failing tests that pin the bug down. Try them on bughunt/fastvector.py."""

from fastvector import Ship, Vector


def test_firing_does_not_change_the_ship_s_velocity():
    ship = Ship(Vector(400, 300))
    ship.fire()
    assert ship.velocity == Vector(0, 0)


def test_a_bullet_s_flight_does_not_move_the_ship():
    ship = Ship(Vector(400, 300))
    bullet = ship.fire()
    bullet.update(0.5)
    assert ship.position == Vector(400, 300)
    assert bullet.position == Vector(610, 300)


def test_plus_equals_does_not_reach_other_names():
    a = b = Vector(1, 1)
    a += Vector(2, 2)
    assert (a, b) == (Vector(3, 3), Vector(1, 1))
