"""Dates and times, as people like to read them."""

from collections import Counter
from datetime import datetime, timedelta

BLOCKS = " ▁▂▃▄▅▆▇█"


def ago(then: datetime, now: datetime) -> str:
    """Say how long ago something happened, roughly, as a person would."""
    seconds = (now - then).total_seconds()
    if seconds < 0:
        return "in the future"
    for size, name in [(86400 * 365, "year"), (86400 * 30, "month"), (86400 * 7, "week"),
                       (86400, "day"), (3600, "hour"), (60, "minute")]:  # fmt: skip
        count = int(seconds // size)
        if count >= 1:
            return f"{count} {name}{'s' if count > 1 else ''} ago"
    return "just now"


def weekly(times: list[datetime], now: datetime, weeks: int) -> list[int]:
    """Count the commits in each of the last so-many weeks, oldest first."""
    counts = Counter((now - time) // timedelta(weeks=1) for time in times)
    return [counts[back] for back in reversed(range(weeks))]


def sparkline(counts: list[int]) -> str:
    """Draw some numbers as a row of little bars: ▁▂▃▄▅▆▇█."""
    tallest = max(counts, default=0)
    if tallest == 0:
        return " " * len(counts)
    return "".join(BLOCKS[-(-count * 8 // tallest)] for count in counts)
