import random
from itertools import islice

import pytest

from asteroids.model import (
    HEIGHT,
    WIDTH,
    Bullet,
    Controls,
    Game,
    Rock,
    Ship,
    State,
    Zone,
    touching,
    waves,
)
from asteroids.vector import Vector

STILL = Controls()


@pytest.fixture
def rng():
    return random.Random(12)


@pytest.fixture
def game(rng):
    """A game that's under way, with the rocks cleared out of the way."""
    game = Game(rng)
    game.start()
    game.rocks.clear()
    return game


def test_touching_works_for_anything_with_a_position_and_a_radius(rng):
    rock = Rock(Vector(100, 100), Vector(), 3, rng)
    assert touching(rock, Zone(Vector(130, 100), 5))
    assert not touching(rock, Zone(Vector(160, 100), 5))
    assert touching(Bullet(Vector(100, 139), Vector()), rock)
    assert touching(Ship(Vector(100, 60)), rock)


def test_a_ship_turns_at_its_turning_speed():
    ship = Ship(Vector(400, 300))
    ship.update(0.5, Controls(turn=1))
    assert ship.heading == 120
    ship.update(1.0, Controls(turn=-1))
    assert ship.heading == 240


def test_thrust_speeds_the_ship_up_the_way_it_is_facing():
    ship = Ship(Vector(400, 300))
    ship.heading = 90
    ship.update(0.1, Controls(thrust=True))
    assert ship.velocity.x > 20
    assert ship.velocity.y == pytest.approx(0, abs=1e-9)
    assert ship.position.x > 400


def test_a_ship_coasts_and_slows_down():
    ship = Ship(Vector(400, 300))
    ship.velocity = Vector(100, 0)
    ship.update(0.5, STILL)
    assert 0 < ship.velocity.x < 100
    assert ship.position.x > 400


def test_a_ship_wraps_round_the_edge_of_the_screen():
    ship = Ship(Vector(WIDTH - 1, 300))
    ship.velocity = Vector(100, 0)
    ship.update(0.1, STILL)
    assert ship.position.x < 20


def test_the_gun_has_to_reload():
    ship = Ship(Vector(400, 300))
    first = ship.fire()
    assert first is not None
    assert ship.fire() is None
    ship.update(Ship.RELOAD, STILL)
    assert ship.fire() is not None


def test_a_bullet_leaves_from_the_nose_with_the_ship_s_speed_added():
    ship = Ship(Vector(400, 300))
    ship.velocity = Vector(50, 0)
    bullet = ship.fire()
    assert bullet.position == Vector(400, 286)
    assert tuple(bullet.velocity) == pytest.approx((50, -Bullet.SPEED))


def test_bullets_do_not_last_for_ever():
    bullet = Bullet(Vector(0, 0), Vector(10, 0))
    bullet.update(Bullet.LIFETIME / 2)
    assert not bullet.spent
    bullet.update(Bullet.LIFETIME / 2)
    assert bullet.spent


def test_a_big_rock_splits_into_two_smaller_faster_ones(rng):
    rock = Rock(Vector(100, 100), Vector(40, 0), 3, rng)
    pieces = rock.split(rng)
    assert [piece.size for piece in pieces] == [2, 2]
    assert all(piece.position == rock.position for piece in pieces)
    assert all(abs(piece.velocity) == pytest.approx(56) for piece in pieces)
    assert pieces[0].velocity != pieces[1].velocity


def test_the_smallest_rocks_just_vanish(rng):
    assert Rock(Vector(), Vector(), 1, rng).split(rng) == []


def test_a_rock_has_a_lumpy_outline_that_turns_with_it(rng):
    rock = Rock(Vector(100, 100), Vector(), 2, rng)
    before = rock.outline()
    assert len(before) == 12
    assert all(15 < abs(point - rock.position) < 28 for point in before)
    rock.update(1.0)
    assert rock.outline() != before


def test_waves_go_on_for_ever_and_get_bigger(rng):
    sizes = [len(rocks) for rocks in islice(waves(rng), 10)]
    assert sizes == [4, 5, 6, 7, 8, 9, 10, 11, 11, 11]


def test_rocks_start_at_the_edge_well_away_from_the_ship(rng):
    centre = Zone(Vector(WIDTH / 2, HEIGHT / 2), 150)
    for rocks in islice(waves(rng), 5):
        assert not any(touching(centre, rock) for rock in rocks)


def test_on_the_title_screen_the_rocks_drift_and_the_ship_does_not(rng):
    game = Game(rng)
    before = [rock.position for rock in game.rocks]
    game.update(1.0, Controls(thrust=True, fire=True))
    assert game.state is State.TITLE
    assert [rock.position for rock in game.rocks] != before
    assert game.ship.position == Vector(WIDTH / 2, HEIGHT / 2)
    assert game.bullets == []


def test_shooting_a_rock_scores_and_splits_it(game, rng):
    game.rocks.append(Rock(Vector(400, 200), Vector(), 3, rng))
    game.update(0.01, Controls(fire=True))
    for _ in range(30):
        game.update(0.01, STILL)
    assert game.score == 20
    assert [rock.size for rock in game.rocks] == [2, 2]
    assert game.bullets == []
    assert game.events == ["fire", "bang"]


def test_hitting_a_rock_costs_a_life_and_clears_a_space(game, rng):
    game.rocks.append(Rock(Vector(405, 300), Vector(), 3, rng))
    game.rocks.append(Rock(Vector(100, 100), Vector(), 3, rng))
    game.update(0.01, STILL)
    assert game.lives == 2
    assert [rock.position for rock in game.rocks] == [Vector(100, 100)]
    assert game.events == ["crash"]


def test_the_last_life_ends_the_game(game, rng):
    for _ in range(3):
        game.rocks.append(Rock(game.ship.position, Vector(), 1, rng))
        game.update(0.01, STILL)
    assert game.state is State.GAME_OVER
    assert game.lives == 0


def test_clearing_the_rocks_brings_the_next_wave(game):
    assert game.wave == 1
    game.update(0.01, STILL)
    assert game.wave == 2
    assert len(game.rocks) == 5
