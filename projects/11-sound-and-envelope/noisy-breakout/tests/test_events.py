from breakout.app import SOUNDS
from breakout.model import Game, Level


def served_game() -> Game:
    game = Game(levels=[Level.from_text("RR"), Level.from_text("G")])
    game.serve()
    return game


def test_a_quiet_frame_has_no_events():
    game = served_game()
    game.update(0.01)
    assert game.events == []


def test_hitting_a_brick_is_an_event():
    game = served_game()
    brick = game.level.bricks[0]
    game.ball.rect.midtop = (brick.rect.centerx, brick.rect.bottom + 1)
    game.ball.vx, game.ball.vy = 0.0, -150
    game.update(0.02)
    assert game.events == ["brick"]


def test_walls_the_bat_and_a_lost_life_are_events():
    game = served_game()
    game.ball.rect.topleft = (1, 120)
    game.ball.vx, game.ball.vy = -100, 0.0
    game.update(0.02)

    game.ball.rect.midbottom = (game.bat.rect.centerx, game.bat.rect.top + 1)
    game.ball.vx, game.ball.vy = 0.0, 100
    game.update(0.001)

    game.ball.rect.top = 300
    game.update(0.01)
    assert game.events == ["wall", "bat", "lost"]


def test_clearing_a_level_is_an_event():
    game = served_game()
    game.level.bricks.clear()
    game.update(0.01)
    assert game.events == ["cleared"]


def test_every_event_has_a_sound():
    for event in ["wall", "bat", "brick", "lost", "cleared"]:
        channel, _, pitch, duration = SOUNDS[event]
        assert 0 <= channel <= 3
        assert 0 <= pitch <= 255
        assert duration > 0
