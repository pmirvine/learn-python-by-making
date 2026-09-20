"""Fetching every feed at once, politely, and without letting one failure spoil the rest."""

import asyncio
import logging
import time
from dataclasses import dataclass, field

import httpx

from newsroom.feeds import Feed, FeedError, Story, parse

log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class Result:
    """How one feed went: its stories, or else what went wrong."""

    feed: Feed
    stories: list[Story] = field(default_factory=list[Story])
    problem: str = ""
    seconds: float = 0.0


async def fetch_one(client: httpx.AsyncClient, feed: Feed) -> list[Story]:
    """Fetch one feed, and parse it. Anything that goes wrong is a FeedError."""
    try:
        response = await client.get(feed.url, follow_redirects=True)
        response.raise_for_status()
    except httpx.HTTPError as error:
        raise FeedError(f"{type(error).__name__}: {error}") from error
    return parse(response.text)


async def attempt(
    client: httpx.AsyncClient, feed: Feed, turnstile: asyncio.Semaphore, patience: float
) -> Result:
    """Fetch one feed, a few at a time, within a time limit, and never raise."""
    async with turnstile:
        started = time.perf_counter()
        try:
            async with asyncio.timeout(patience):
                stories = await fetch_one(client, feed)
        except FeedError as error:
            return Result(
                feed, problem=str(error), seconds=time.perf_counter() - started
            )
        except TimeoutError:
            problem = f"no answer in {patience:g} seconds"
            return Result(feed, problem=problem, seconds=time.perf_counter() - started)
        return Result(feed, stories, seconds=time.perf_counter() - started)


async def fetch_all(
    client: httpx.AsyncClient, feeds: list[Feed], at_once: int = 4, patience: float = 10
) -> list[Result]:
    """Fetch all the feeds, no more than a few at a time. Return a result for each."""
    turnstile = asyncio.Semaphore(at_once)
    async with asyncio.TaskGroup() as group:
        tasks = [
            group.create_task(attempt(client, feed, turnstile, patience))
            for feed in feeds
        ]
    results = [task.result() for task in tasks]
    failed = sum(1 for result in results if result.problem)
    log.info("Fetched %d feeds, of which %d failed", len(results), failed)
    return results
