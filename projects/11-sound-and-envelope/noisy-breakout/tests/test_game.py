from dataclasses import FrozenInstanceError, replace

import pytest

from breakout.model import Game, Level, Settings, State


@pytest.fixture
def game():
    """A game with two very small levels, waiting for the first serve."""
    return Game(levels=[Level.from_text("RR", "one"), Level.from_text("#", "two")])


def test_the_ball_rides_on_the_bat_until_it_is_served(game):
    game.update(0.1, steer=1)
    assert game.state is State.SERVE
    assert game.ball.rect.midbottom == game.bat.rect.midtop
    assert game.bat.rect.centerx == 186


def test_serving_launches_the_ball_upwards(game):
    game.serve()
    assert game.state is State.PLAYING
    assert game.ball.vy < 0
    before = game.ball.rect.top
    game.update(0.02)
    assert game.ball.rect.top < before


def test_the_ball_bounces_off_the_side_walls(game):
    game.serve()
    game.ball.rect.topleft = (1, 120)
    game.ball.vx, game.ball.vy = -100, 0.0
    game.update(0.02)
    assert game.ball.vx == 100
    assert game.ball.rect.left >= 0


def test_the_ball_bounces_off_the_ceiling(game):
    game.serve()
    game.ball.rect.topleft = (150, 1)
    game.ball.vx, game.ball.vy = 0.0, -100
    game.update(0.02)
    assert game.ball.vy == 100


def test_where_the_ball_hits_the_bat_decides_where_it_goes(game):
    game.serve()
    game.ball.rect.midbottom = (game.bat.rect.right - 2, game.bat.rect.top + 1)
    game.ball.vx, game.ball.vy = 0.0, 100
    game.update(0.001)
    assert game.ball.vy < 0
    assert game.ball.vx > 0


def test_hitting_a_brick_scores_and_bounces_and_speeds_up(game):
    game.serve()
    brick = game.level.bricks[0]
    game.ball.rect.midtop = (brick.rect.centerx, brick.rect.bottom + 1)
    game.ball.vx, game.ball.vy = 0.0, -150
    game.update(0.02)
    assert game.score == 50
    assert game.ball.vy > 150
    assert len(game.level.bricks) == 1


def test_missing_the_ball_costs_a_life(game):
    game.serve()
    game.ball.rect.top = 300
    game.update(0.01)
    assert game.lives == 2
    assert game.state is State.SERVE


def test_the_last_life(game):
    for _ in range(3):
        game.serve()
        game.ball.rect.top = 300
        game.update(0.01)
    assert game.state is State.GAME_OVER
    game.update(1.0, steer=1)
    assert game.bat.rect.centerx == 160


def test_clearing_a_level_moves_on_to_the_next(game):
    game.serve()
    game.level.bricks.clear()
    game.update(0.01)
    assert game.number == 1
    assert game.level.name == "two"
    assert game.state is State.SERVE


def test_clearing_the_last_level_wins(game):
    game.serve()
    for _ in range(2):
        game.level.bricks.clear()
        game.state = State.PLAYING
        game.update(0.01)
    assert game.state is State.WON


def test_starting_again_rebuilds_the_walls(game):
    game.serve()
    game.level.bricks.clear()
    game.update(0.01)
    game.state = State.GAME_OVER
    game.serve()
    assert (game.number, game.score, game.lives) == (0, 0, 3)
    assert len(game.level.bricks) == 2


def test_settings_cannot_be_changed_but_can_be_varied():
    settings = Settings()
    with pytest.raises(FrozenInstanceError):
        settings.lives = 99
    hard = replace(settings, lives=1, bat_width=24)
    assert Game(levels=[Level.from_text("R")], settings=hard).lives == 1
    assert settings.lives == 3
