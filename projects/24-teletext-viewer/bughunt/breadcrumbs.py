"""A colleague wants the viewer to show where you've been. It never changes.

    uv run bughunt/breadcrumbs.py

It uses the Watched descriptor from the type-in listing, which behaves as
Textual's `reactive` does in the way that matters here.
"""


class Watched:
    def __init__(self, default):
        self.default = default

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, self.default)

    def __set__(self, instance, value):
        old = self.__get__(instance)
        instance.__dict__[self.name] = value
        watcher = getattr(instance, f"watch_{self.name}", None)
        if watcher and value != old:
            watcher(old, value)


class Trail:
    """Keeps the pages that have been visited, and shows them when they change."""

    visited = Watched([100])

    def __init__(self) -> None:
        self.shown = "Trail: 100"

    def watch_visited(self, old: list[int], new: list[int]) -> None:
        self.shown = "Trail: " + " > ".join(str(number) for number in new)

    def visit(self, number: int) -> None:
        self.visited.append(number)


def main() -> None:
    trail = Trail()
    for number in (101, 301, 500):
        trail.visit(number)
        print(f"Went to {number}.  {trail.shown}")
    print()
    print("A second viewer, which hasn't been anywhere yet:", Trail().visited)


if __name__ == "__main__":
    main()
