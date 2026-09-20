"""The failing test that pins the steering bug down. Try it on bughunt/duel.py."""

from duel import Cycle, Direction


def test_each_cycle_steers_itself():
    one = Cycle((24, 36), Direction.RIGHT, "yellow")
    two = Cycle((72, 36), Direction.LEFT, "cyan")

    two.turn(Direction.UP)
    one.advance()
    two.advance()

    assert one.heading is Direction.RIGHT
    assert two.heading is Direction.UP


def test_cycles_do_not_share_a_queue():
    one = Cycle((0, 0), Direction.RIGHT, "yellow")
    two = Cycle((9, 9), Direction.LEFT, "cyan")
    assert one.turns is not two.turns
