from datetime import UTC, datetime, timedelta

import pytest

from dashboard.when import ago, sparkline, weekly

NOW = datetime(2026, 9, 20, 12, 0, tzinfo=UTC)


@pytest.mark.parametrize(
    ("before", "words"),
    [
        (timedelta(seconds=5), "just now"),
        (timedelta(minutes=1), "1 minute ago"),
        (timedelta(minutes=59, seconds=59), "59 minutes ago"),
        (timedelta(hours=2), "2 hours ago"),
        (timedelta(days=1), "1 day ago"),
        (timedelta(days=3, hours=2), "3 days ago"),
        (timedelta(days=13), "1 week ago"),
        (timedelta(days=45), "1 month ago"),
        (timedelta(days=800), "2 years ago"),
        (timedelta(days=-1), "in the future"),
    ],
)
def test_ago(before, words):
    assert ago(NOW - before, NOW) == words


def test_ago_works_across_time_zones():
    tokyo = datetime.fromisoformat("2026-09-20T20:00:00+09:00")
    assert ago(tokyo, NOW) == "1 hour ago"


def test_naive_and_aware_times_cannot_be_mixed():
    with pytest.raises(TypeError, match="offset-naive and offset-aware"):
        ago(datetime(2026, 9, 20, 11, 0), NOW)  # noqa: DTZ001


def test_weekly():
    times = [NOW - timedelta(days=days) for days in (0, 1, 6, 7, 20, 100)]
    assert weekly(times, NOW, 4) == [0, 1, 1, 3]
    assert weekly([], NOW, 3) == [0, 0, 0]


def test_sparkline():
    assert sparkline([0, 1, 4, 8]) == " ▁▄█"
    assert sparkline([0, 0]) == "  "
    assert sparkline([5]) == "█"
    assert sparkline([1, 100]) == "▁█"
