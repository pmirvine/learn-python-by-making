from datetime import UTC, date, datetime

from streak import current_streak, longest_streak


def at(day: int, hour: int = 12) -> datetime:
    return datetime(2026, 3, day, hour, tzinfo=UTC)


def test_the_longest_streak():
    commits = [at(1), at(2), at(2, 18), at(3), at(7), at(8), at(20)]
    assert longest_streak(commits) == 3
    assert longest_streak([]) == 0
    assert longest_streak([at(5)]) == 1


def test_a_streak_runs_across_the_end_of_a_month():
    commits = [datetime(2026, 2, 28, tzinfo=UTC), datetime(2026, 3, 1, tzinfo=UTC)]
    assert longest_streak(commits) == 2


def test_the_current_streak_may_end_today_or_yesterday():
    commits = [at(5), at(6), at(7)]
    assert current_streak(commits, date(2026, 3, 7)) == 3
    assert current_streak(commits, date(2026, 3, 8)) == 3
    assert current_streak(commits, date(2026, 3, 9)) == 0
