"""The failing tests for the colleague's `ago`. The real one passes them."""

from datetime import UTC, datetime, timedelta

import pytest

from dashboard.when import ago

NOW = datetime(2026, 9, 20, 12, 0, tzinfo=UTC)


@pytest.mark.parametrize(
    ("gap", "words"),
    [
        (timedelta(days=3, minutes=5), "3 days ago"),
        (timedelta(days=400, seconds=10), "1 year ago"),
        (timedelta(days=2, hours=6), "2 days ago"),
    ],
)
def test_the_days_count_for_something(gap, words):
    assert ago(NOW - gap, NOW) == words
