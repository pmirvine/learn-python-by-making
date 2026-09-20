"""Regenerate the Project 23 picture, which is an SVG that Rich itself writes.

uv run --project projects/23-rich-dashboard python scripts/screenshots_p23.py
"""

import io
import random
from datetime import UTC, datetime, timedelta
from pathlib import Path

from dashboard.stats import Project
from dashboard.view import dashboard
from rich.console import Console

ASSETS = Path(__file__).parent.parent / "docs" / "assets"
NOW = datetime(2026, 9, 20, 12, 0, tzinfo=UTC)
NAMES = [
    "hi-lo",
    "dice-lab",
    "cupboard",
    "life",
    "beeb",
    "snake",
    "breakout",
    "asteroids",
]


def made_up(name: str, number: int, rng: random.Random) -> Project:
    """Invent a plausible history: a fortnight of work, some weeks ago."""
    started = NOW - timedelta(weeks=11 - number * 1.4)
    commits = [
        started + timedelta(days=rng.uniform(0, 12), hours=rng.uniform(-3, 3))
        for _ in range(rng.randint(6, 30))
    ]
    commits = [commit for commit in commits if commit < NOW]
    changed = 2 if name == "asteroids" else 0
    lines, tests = rng.randint(150, 1200), rng.randint(0, 45)
    return Project(name, Path(name), commits, "main", changed, lines, tests)


def main() -> None:
    rng = random.Random(23)
    projects = [made_up(name, number, rng) for number, name in enumerate(NAMES)]
    console = Console(record=True, width=100, file=io.StringIO())
    console.print(dashboard(projects, NOW, "recent", weeks=12))
    svg = console.export_svg(title="uv run dashboard ~/making --sort recent")
    (ASSETS / "p23-dashboard.svg").write_text(svg, encoding="utf-8")
    print("Saved p23-dashboard.svg")


if __name__ == "__main__":
    main()
