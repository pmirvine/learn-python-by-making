"""The failing test that pins the bug down. Run it against bughunt/lines.py first."""

from lines import remember, step


def test_the_trail_remembers_where_the_line_has_been():
    line = [100.0, 100.0, 200.0, 200.0]
    velocity = [10.0, 10.0, 10.0, 10.0]
    trail = []

    for _ in range(3):
        step(line, velocity)
        remember(trail, line, 1)

    positions = [position for position, _ in trail]
    assert positions == [
        [110.0, 110.0, 210.0, 210.0],
        [120.0, 120.0, 220.0, 220.0],
        [130.0, 130.0, 230.0, 230.0],
    ]
