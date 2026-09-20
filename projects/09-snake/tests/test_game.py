import random

import pytest

from snake.model import Direction, Game, State


@pytest.fixture
def game():
    """A game in progress, with dice that always fall the same way."""
    game = Game(columns=20, rows=10, rng=random.Random(1))
    game.start()
    return game


def test_a_new_game_waits_on_the_title_screen():
    game = Game()
    assert game.state is State.TITLE
    game.update(10.0)
    assert game.snake.head() == (16, 12)


def test_the_snake_steps_only_when_enough_time_has_gone_by(game):
    game.update(0.10)
    assert game.snake.head() == (10, 5)
    game.update(0.05)
    assert game.snake.head() == (11, 5)


def test_a_long_frame_means_several_steps(game):
    game.update(game.interval * 3)
    assert game.snake.head() == (13, 5)


def test_pausing_stops_the_clock(game):
    game.toggle_pause()
    assert game.state is State.PAUSED
    game.update(5.0)
    game.turn(Direction.UP)
    assert game.snake.head() == (10, 5)
    assert not game.snake.turns
    game.toggle_pause()
    assert game.state is State.PLAYING


def test_hitting_the_wall_ends_the_game(game):
    for _ in range(10):
        game.step()
    assert game.state is State.GAME_OVER


def test_food_is_never_placed_on_the_snake(game):
    for _ in range(200):
        assert game.free_cell() not in game.snake.body


def test_eating_scores_and_grows_and_speeds_up(game):
    game.food = (11, 5)
    before = game.interval
    game.step()
    assert game.score == 10
    assert game.snake.growing == 1
    assert game.interval < before
    assert game.food != (11, 5)


def test_the_best_score_survives_a_new_round(game):
    game.food = (11, 5)
    game.step()
    while game.state is State.PLAYING:
        game.step()
    assert game.best == 10

    game.start()
    assert game.state is State.PLAYING
    assert (game.score, game.best) == (0, 10)
    assert game.snake.head() == (10, 5)


def test_two_games_do_not_share_anything():
    first, second = Game(rng=random.Random(1)), Game(rng=random.Random(1))
    first.start()
    first.update(1.0)
    assert second.state is State.TITLE
    assert second.snake.head() == (16, 12)
