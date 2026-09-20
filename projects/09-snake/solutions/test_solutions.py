import random

from model import Game, State
from two_player import loser

from snake.model import Direction, Snake


def test_nobody_has_lost_at_the_start():
    assert loser([Snake((12, 18)), Snake((36, 18), Direction.LEFT)]) is None


def test_running_into_the_other_snake_loses():
    one = Snake((12, 18))
    two = Snake((13, 25), Direction.UP)
    for _ in range(7):
        two.advance()
    assert two.head() == (13, 18)
    one.advance()
    assert loser([one, two]) == 0


def test_a_wrapping_game_has_no_walls():
    game = Game(columns=20, rows=10, rng=random.Random(1), wrap=True)
    game.start()
    for _ in range(25):
        game.step()
    assert game.state is State.PLAYING
    assert game.snake.head() == (15, 5)


def test_without_the_option_the_walls_are_still_there():
    game = Game(columns=20, rows=10, rng=random.Random(1))
    game.start()
    for _ in range(25):
        game.step()
    assert game.state is State.GAME_OVER


def test_a_snake_counts_its_meals():
    game = Game(columns=20, rows=10, rng=random.Random(1), wrap=True)
    game.start()
    game.food = (11, 5)
    game.step()
    assert game.snake.meals == 1
    assert game.score == 10
