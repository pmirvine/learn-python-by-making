"""Extend 1: try again, a little later each time, before giving a feed up for lost."""

import asyncio
import random
from collections.abc import Awaitable, Callable

from newsroom.feeds import FeedError


async def with_retries[T](
    action: Callable[[], Awaitable[T]],
    attempts: int = 3,
    first_wait: float = 0.5,
    rng: random.Random | None = None,
) -> T:
    """Call an async function until it works, waiting twice as long after each failure.

    The waits are made a little uneven, so that a hundred clients that all failed
    at the same moment don't all come back at the same moment too.
    """
    rng = rng or random.Random()
    wait = first_wait
    for attempt in range(1, attempts + 1):
        try:
            return await action()
        except FeedError:
            if attempt == attempts:
                raise
        await asyncio.sleep(wait * rng.uniform(0.5, 1.5))
        wait *= 2
    raise AssertionError("unreachable")
