from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from rich.console import Console

from dashboard.stats import Project
from dashboard.view import SORTS, dashboard

NOW = datetime(2026, 9, 20, 12, 0, tzinfo=UTC)


def project(name: str, days_ago: list[int], lines: int, tests: int) -> Project:
    commits = [NOW - timedelta(days=days) for days in days_ago]
    return Project(name, Path(name), commits, "main", 0, lines, tests)


PROJECTS = [
    project("snake", [1, 2, 3], lines=800, tests=31),
    project("asteroids", [40], lines=900, tests=12),
    project("hi-lo", [], lines=200, tests=0),
]


def shown(order: str) -> str:
    console = Console(record=True, width=120)
    console.print(dashboard(PROJECTS, NOW, order, weeks=8))
    return console.export_text()


@pytest.mark.parametrize(
    ("order", "names"),
    [
        ("name", ["asteroids", "hi-lo", "snake"]),
        ("recent", ["snake", "asteroids", "hi-lo"]),
        ("commits", ["snake", "asteroids", "hi-lo"]),
        ("lines", ["asteroids", "snake", "hi-lo"]),
        ("tests", ["snake", "asteroids", "hi-lo"]),
    ],
)
def test_every_way_of_sorting(order, names):
    assert sorted(PROJECTS, key=SORTS[order]) == [
        next(project for project in PROJECTS if project.name == name) for name in names
    ]


def test_what_is_on_the_screen():
    text = shown("name")
    assert "Sorted by name" in text
    assert "1 day ago" in text
    assert "never" in text
    assert "3 projects" in text
    assert "1,900" in text
    assert text.index("asteroids") < text.index("hi-lo") < text.index("snake")


def test_files_that_have_changed_are_flagged():
    busy = project("busy", [0], 10, 1)
    busy.changed = 3
    console = Console(record=True, width=120)
    console.print(dashboard([busy], NOW))
    assert "main +3" in console.export_text()
