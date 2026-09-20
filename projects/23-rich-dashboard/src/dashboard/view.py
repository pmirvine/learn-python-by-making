"""Showing it all, with Rich."""

from collections.abc import Callable
from datetime import datetime
from operator import attrgetter

from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from dashboard.stats import Project, busiest_day
from dashboard.when import ago, sparkline, weekly


def newest_first(project: Project) -> float:
    """A sort key: the time of the latest commit, as a number, or 0 if there isn't one."""
    return -project.latest.timestamp() if project.latest else 0.0


# Each way of sorting is a function that takes a project and returns what to sort by.
SORTS: dict[str, Callable[[Project], str | float]] = {
    "name": attrgetter("name"),
    "recent": newest_first,
    "commits": lambda project: -len(project.commits),
    "lines": lambda project: -project.lines,
    "tests": lambda project: -project.tests,
}


def table(projects: list[Project], now: datetime, order: str, weeks: int) -> Table:
    grid = Table(title=f"Sorted by {order}", title_justify="left", expand=True)
    grid.add_column("Project", style="bold cyan", no_wrap=True)
    grid.add_column("Branch")
    grid.add_column("Commits", justify="right")
    grid.add_column("Last commit")
    grid.add_column("Lines", justify="right")
    grid.add_column("Tests", justify="right")
    grid.add_column(f"Last {weeks} weeks", style="green", no_wrap=True)

    for project in sorted(projects, key=SORTS[order]):
        branch = Text(project.branch or "not in Git", style="dim")
        if project.changed:
            branch = Text(f"{project.branch} +{project.changed}", style="yellow")
        grid.add_row(
            Text(project.name),  # a Text is never read as markup, whatever it's called
            branch,
            f"{len(project.commits):,}",
            ago(project.latest, now) if project.latest else "never",
            f"{project.lines:,}",
            f"{project.tests:,}",
            sparkline(weekly(project.commits, now, weeks)),
        )

    grid.add_section()
    grid.add_row(
        f"{len(projects)} projects",
        "",
        f"{sum(len(project.commits) for project in projects):,}",
        "",
        f"{sum(project.lines for project in projects):,}",
        f"{sum(project.tests for project in projects):,}",
        "",
        style="bold",
    )
    return grid


def dashboard(
    projects: list[Project], now: datetime, order: str = "name", weeks: int = 12
) -> RenderableType:
    """Return the whole display, ready for a console to print."""
    days = sum(project.days_worked for project in projects)
    summary = Text.assemble(
        "Your busiest day is ",
        (busiest_day(projects), "bold magenta"),
        f". {days} project-days of work so far.",
    )
    return Group(
        Panel(summary, title="Learn Python by making"),
        table(projects, now, order, weeks),
    )
