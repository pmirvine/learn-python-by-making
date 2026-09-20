"""The failing tests for the colleague's trail, and a mended trail that passes them."""

import importlib.util
from pathlib import Path

HUNT = Path(__file__).parent.parent.parent / "bughunt" / "breadcrumbs.py"
spec = importlib.util.spec_from_file_location("breadcrumbs", HUNT)
assert spec is not None
assert spec.loader is not None
breadcrumbs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(breadcrumbs)
Watched = breadcrumbs.Watched


class Trail:
    visited = Watched((100,))  # a tuple can't be changed, and so it's safe to share

    def __init__(self) -> None:
        self.shown = "Trail: 100"

    def watch_visited(self, old: tuple[int, ...], new: tuple[int, ...]) -> None:
        self.shown = "Trail: " + " > ".join(str(number) for number in new)

    def visit(self, number: int) -> None:
        self.visited = (
            *self.visited,
            number,
        )  # a new value, and so the watcher is told


def test_the_display_follows_the_trail():
    trail = Trail()
    trail.visit(101)
    trail.visit(301)
    assert trail.shown == "Trail: 100 > 101 > 301"


def test_two_viewers_have_two_trails():
    first, second = Trail(), Trail()
    first.visit(101)
    assert second.visited == (100,)


def test_the_colleagues_trail_has_both_faults():
    first, second = breadcrumbs.Trail(), breadcrumbs.Trail()
    first.visit(101)
    assert first.shown == "Trail: 100"
    assert second.visited == [100, 101]
