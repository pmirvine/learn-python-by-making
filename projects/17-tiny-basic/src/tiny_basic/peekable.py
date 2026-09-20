"""An iterator that lets you look at what's coming, without taking it."""

from collections.abc import Iterable, Iterator


class Peekable[T]:
    """Wrap any iterable, and add `peek`.

    It's an iterator in its own right, since it has `__iter__` and `__next__`,
    and so it works in a `for` loop, or with `next`, or with `list`.
    """

    def __init__(self, items: Iterable[T]) -> None:
        self._items: Iterator[T] = iter(items)
        self._ahead: list[T] = []  # the item that's been peeked at, if any

    def __iter__(self) -> "Peekable[T]":
        return self

    def __next__(self) -> T:
        if self._ahead:
            return self._ahead.pop()
        return next(self._items)

    def peek(self) -> T | None:
        """Return the next item without using it up, or None if there are no more."""
        if not self._ahead:
            try:
                self._ahead.append(next(self._items))
            except StopIteration:
                return None
        return self._ahead[0]
