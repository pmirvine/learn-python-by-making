from snake.model import Direction, Snake


def test_a_new_snake_lies_behind_its_head():
    snake = Snake((10, 5))
    assert list(snake.body) == [(10, 5), (9, 5), (8, 5), (7, 5)]
    assert snake.head() == (10, 5)


def test_a_snake_can_start_out_facing_any_way():
    snake = Snake((10, 5), Direction.UP)
    assert list(snake.body) == [(10, 5), (10, 6), (10, 7), (10, 8)]


def test_advancing_moves_the_head_and_drags_the_tail():
    snake = Snake((10, 5))
    snake.advance()
    assert list(snake.body) == [(11, 5), (10, 5), (9, 5), (8, 5)]


def test_a_turn_takes_effect_at_the_next_step():
    snake = Snake((10, 5))
    snake.turn(Direction.DOWN)
    assert snake.heading is Direction.RIGHT
    snake.advance()
    assert snake.heading is Direction.DOWN
    assert snake.head() == (10, 6)


def test_a_snake_cannot_turn_back_on_itself():
    snake = Snake((10, 5))
    snake.turn(Direction.LEFT)
    snake.advance()
    assert snake.head() == (11, 5)


def test_two_quick_turns_are_both_remembered():
    snake = Snake((10, 5))
    snake.turn(Direction.UP)
    snake.turn(Direction.LEFT)
    snake.advance()
    snake.advance()
    assert snake.head() == (9, 4)


def test_a_reversal_cannot_be_smuggled_in_behind_a_quick_turn():
    snake = Snake((10, 5))
    snake.turn(Direction.UP)
    snake.turn(Direction.DOWN)
    assert list(snake.turns) == [Direction.UP]


def test_growing_keeps_the_tail_where_it_is():
    snake = Snake((10, 5))
    snake.grow(2)
    snake.advance()
    snake.advance()
    snake.advance()
    assert len(snake.body) == 6
    assert snake.body[-1] == (8, 5)


def test_a_long_snake_can_bite_itself():
    snake = Snake((10, 5))
    snake.grow(4)
    for direction in (Direction.DOWN, Direction.LEFT, Direction.UP):
        snake.turn(direction)
        snake.advance()
    assert snake.bites_itself()


def test_every_snake_has_a_body_of_its_own():
    first, second = Snake((5, 5)), Snake((20, 20))
    first.advance()
    first.turn(Direction.UP)
    assert second.head() == (20, 20)
    assert not second.turns
    assert first.body is not second.body


def test_opposites():
    assert Direction.UP.opposite() is Direction.DOWN
    assert Direction.LEFT.opposite() is Direction.RIGHT
