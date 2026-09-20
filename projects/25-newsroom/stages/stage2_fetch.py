"""Fetching every feed at once. (Stage 2: all or nothing.)"""

import asyncio

import httpx

from newsroom.feeds import Feed, FeedError, Story, parse


async def fetch_one(client: httpx.AsyncClient, feed: Feed) -> list[Story]:
    """Fetch one feed, and parse it. Anything that goes wrong is a FeedError."""
    try:
        response = await client.get(feed.url, follow_redirects=True)
        response.raise_for_status()
    except httpx.HTTPError as error:
        raise FeedError(f"{type(error).__name__}: {error}") from error
    return parse(response.text)


async def fetch_all(client: httpx.AsyncClient, feeds: list[Feed]) -> list[list[Story]]:
    """Fetch all the feeds at once. If any of them fails, the whole thing fails."""
    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(fetch_one(client, feed)) for feed in feeds]
    return [task.result() for task in tasks]
