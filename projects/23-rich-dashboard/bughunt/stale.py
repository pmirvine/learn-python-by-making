"""A colleague's way of saying how long ago something was. Old projects look too fresh.

uv run bughunt/stale.py
"""

from datetime import UTC, datetime, timedelta


def ago(then: datetime, now: datetime) -> str:
    """Say how long ago something happened."""
    gap = now - then
    if gap.seconds < 60:
        return "just now"
    if gap.seconds < 3600:
        return f"{gap.seconds // 60} minutes ago"
    if gap.days < 1:
        return f"{gap.seconds // 3600} hours ago"
    return f"{gap.days} days ago"


def main() -> None:
    now = datetime(2026, 9, 20, 12, 0, tzinfo=UTC)
    for gap in [
        timedelta(minutes=5),
        timedelta(hours=3),
        timedelta(days=2, hours=6),
        timedelta(days=3, minutes=5),
        timedelta(days=400, seconds=10),
    ]:
        print(f"{gap!s:>20}  ->  {ago(now - gap, now)}")


if __name__ == "__main__":
    main()
