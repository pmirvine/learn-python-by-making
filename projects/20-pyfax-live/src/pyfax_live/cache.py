"""Remembering an answer for a while, so as not to ask for it too often."""

import logging
import time
from collections.abc import Callable

log = logging.getLogger(__name__)


class TimedCache[K, V]:
    """Keep each value for so many seconds. After that, the next caller fetches a new one.

    If the fetching fails, and there's an old value to hand, the old value is
    served, since a forecast that's an hour old is better than none.
    """

    def __init__(
        self, seconds: float, clock: Callable[[], float] = time.monotonic
    ) -> None:
        self.seconds = seconds
        self.clock = clock
        self.kept: dict[K, tuple[float, V]] = {}

    def get(self, key: K, fetch: Callable[[], V]) -> V:
        now = self.clock()
        if key in self.kept:
            when, value = self.kept[key]
            if now - when < self.seconds:
                return value
        try:
            value = fetch()
        except Exception:
            if key not in self.kept:
                raise
            log.warning("Couldn't fetch %s. Serving the old one.", key, exc_info=True)
            return self.kept[key][1]
        self.kept[key] = (now, value)
        return value
