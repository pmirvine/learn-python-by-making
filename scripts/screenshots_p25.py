"""Regenerate the Project 25 pictures, from made-up feeds, with no network.

uv run --project projects/25-newsroom python scripts/screenshots_p25.py
"""

import asyncio
from datetime import UTC, datetime
from pathlib import Path

import httpx
from newsroom.app import Newsroom
from newsroom.feeds import Feed
from teleview.glyphs import quadrant

ROOT = Path(__file__).parent.parent
ASSETS = ROOT / "docs" / "assets"
FEEDS = ROOT / "projects" / "25-newsroom" / "tests" / "feeds"
NOON = datetime(2026, 9, 20, 12, 0, 0, tzinfo=UTC)
FOLLOWED = [
    Feed("Little Snoring Gazette", "https://gazette.example/rss"),
    Feed("Turtle Fanciers' Weekly", "https://turtles.example/atom"),
    Feed("The Daily Outage", "https://broken.example/feed"),
    Feed("Gazette: sport", "https://gazette.example/sport"),
]


async def reply(request: httpx.Request) -> httpx.Response:
    await asyncio.sleep(0.01)
    if request.url.host == "gazette.example":
        return httpx.Response(200, text=(FEEDS / "hedgehog.rss").read_text("utf-8"))
    if request.url.host == "turtles.example":
        return httpx.Response(200, text=(FEEDS / "turtle.atom").read_text("utf-8"))
    return httpx.Response(503)


async def shoot(name: str, *keys: str) -> None:
    async with httpx.AsyncClient(transport=httpx.MockTransport(reply)) as client:
        app = Newsroom(FOLLOWED, client, clock=lambda: NOON, glyph=quadrant)
        async with app.run_test(size=(60, 30)) as pilot:
            await app.workers.wait_for_complete()
            await pilot.press(*keys)
            await pilot.pause()
            svg = app.export_screenshot(title="uv run newsroom")
    (ASSETS / name).write_text(svg, encoding="utf-8")


def main() -> None:
    asyncio.run(shoot("p25-index.svg"))
    asyncio.run(shoot("p25-gazette.svg", "1", "0", "1"))
    print("Saved p25-index.svg and p25-gazette.svg")


if __name__ == "__main__":
    main()
