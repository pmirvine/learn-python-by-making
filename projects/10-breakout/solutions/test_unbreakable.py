from unbreakable import Level


def test_unbreakable_bricks_stop_the_ball_but_never_break():
    level = Level.from_text("=")
    target = level.bricks[0].rect
    for _ in range(10):
        assert level.hit_by(target) is not None
    assert len(level.bricks) == 1


def test_a_level_is_cleared_when_only_unbreakable_bricks_are_left():
    level = Level.from_text("=R=")
    assert not level.cleared
    red = level.bricks[1]
    level.hit_by(red.rect)
    assert level.cleared


def test_an_ordinary_level_still_clears():
    level = Level.from_text("G")
    level.hit_by(level.bricks[0].rect)
    assert level.cleared
