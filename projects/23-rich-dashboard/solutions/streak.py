"""Extend 1: streaks. For how many days in a row have you committed something?"""

from datetime import date, datetime, timedelta

ONE_DAY = timedelta(days=1)


def days_of(commits: list[datetime]) -> set[date]:
    """Return the dates on which there was a commit, by the committer's own clock."""
    return {commit.date() for commit in commits}


def longest_streak(commits: list[datetime]) -> int:
    """Return the length of the longest run of days in a row."""
    days = days_of(commits)
    best = 0
    for day in days:
        if day - ONE_DAY in days:
            continue  # this day isn't the start of a run
        length = 1
        while day + length * ONE_DAY in days:
            length += 1
        best = max(best, length)
    return best


def current_streak(commits: list[datetime], today: date) -> int:
    """Return the run that's still going: it must reach today, or yesterday."""
    days = days_of(commits)
    day = today if today in days else today - ONE_DAY
    length = 0
    while day in days:
        length += 1
        day -= ONE_DAY
    return length
