"""The failing test that pins the census bug down. Try it on bughunt/census.py."""

from census import peak, report

from life import PATTERNS, parse


def test_the_report_ends_with_the_peak():
    lines = report(parse(PATTERNS["blinker"]), 5)
    assert len(lines) == 6
    assert lines[0] == "   0 █ 3"
    assert lines[-1] == "Peak population: 3"


def test_peak_is_happy_with_a_list():
    assert peak([{(0, 0)}, {(0, 0), (1, 1)}, set()]) == 2
