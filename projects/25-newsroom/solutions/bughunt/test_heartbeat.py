"""The failing test for the colleague's fetch, and a mended fetch that passes it."""

import asyncio
import time
from collections.abc import Awaitable, Callable
from itertools import pairwise


def slow_download(name: str) -> str:
    time.sleep(0.2)
    return f"<rss>{name}</rss>"


async def fetch(name: str) -> str:
    """The blocking call is sent to a thread, and the event loop is left free."""
    return await asyncio.to_thread(slow_download, name)


async def blocking_fetch(name: str) -> str:
    """The colleague's version: async in name only."""
    return slow_download(name)


async def longest_gap_during(
    work: Callable[[], Awaitable[object]],
) -> tuple[float, float]:
    """Do some work with a heart beating beside it. Return the longest pause
    between two beats, and how long the work took."""
    beats: list[float] = []

    async def heart() -> None:
        while True:
            beats.append(time.perf_counter())
            await asyncio.sleep(0.01)

    beating = asyncio.create_task(heart())
    await asyncio.sleep(0.05)
    started = time.perf_counter()
    await work()
    took = time.perf_counter() - started
    await asyncio.sleep(0.05)
    beating.cancel()
    return max(later - earlier for earlier, later in pairwise(beats)), took


async def test_the_heart_keeps_beating_and_the_feeds_really_are_fetched_at_once():
    names = ("news", "weather", "sport")
    longest_gap, took = await longest_gap_during(
        lambda: asyncio.gather(*(fetch(name) for name in names))
    )
    assert longest_gap < 0.1
    assert took < 0.4  # and not 3 x 0.2 = 0.6 seconds


async def test_whereas_a_blocking_call_in_a_coroutine_stops_everything():
    names = ("news", "weather", "sport")
    longest_gap, took = await longest_gap_during(
        lambda: asyncio.gather(*(blocking_fetch(name) for name in names))
    )
    assert longest_gap > 0.5
    assert took > 0.5
