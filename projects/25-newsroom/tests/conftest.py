import asyncio
from pathlib import Path

import httpx
import pytest

from newsroom.feeds import Feed

FEEDS = Path(__file__).parent / "feeds"

GAZETTE = Feed("Gazette", "https://gazette.example/rss")
TURTLES = Feed("Turtles", "https://turtles.example/atom")
BROKEN = Feed("Broken", "https://broken.example/feed")
ASLEEP = Feed("Asleep", "https://asleep.example/feed")


class FakeWeb:
    """Stands in for the internet. Every reply takes a while, as real ones do."""

    def __init__(self, delay: float = 0.05) -> None:
        self.delay = delay
        self.busy = 0
        self.busiest = 0
        self.asked: list[str] = []

    async def __call__(self, request: httpx.Request) -> httpx.Response:
        self.asked.append(request.url.host)
        self.busy += 1
        self.busiest = max(self.busiest, self.busy)
        try:
            return await self.reply(request.url.host)
        finally:
            self.busy -= 1

    async def reply(self, host: str) -> httpx.Response:
        if host == "asleep.example":
            await asyncio.sleep(60)
        await asyncio.sleep(self.delay)
        if host == "gazette.example":
            return httpx.Response(200, text=(FEEDS / "hedgehog.rss").read_text("utf-8"))
        if host == "turtles.example":
            return httpx.Response(200, text=(FEEDS / "turtle.atom").read_text("utf-8"))
        return httpx.Response(503, text="Service unavailable")


@pytest.fixture
def web() -> FakeWeb:
    return FakeWeb()


@pytest.fixture
async def client(web: FakeWeb):
    """An async fixture: it has an `async with` in it, and the test gets what it yields."""
    async with httpx.AsyncClient(transport=httpx.MockTransport(web)) as client:
        yield client
