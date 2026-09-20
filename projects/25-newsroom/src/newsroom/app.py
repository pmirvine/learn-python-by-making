"""A teletext newsroom: a dozen live feeds, fetched at once, with asyncio."""

import argparse
import time
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import ClassVar

import httpx
from teleview.app import Viewer, local_time
from teleview.glyphs import GLYPHS
from textual import work
from textual.binding import Binding, BindingType

from newsroom.feeds import Feed, FeedError, load_feeds
from newsroom.fetch import fetch_all
from newsroom.pages import site

AGENT = {"User-Agent": "newsroom/0.1 (a tutorial project)"}


class Newsroom(Viewer):
    """Project 24's viewer, whose pages are fetched, and fetched again every so often."""

    BINDINGS: ClassVar[list[BindingType]] = [
        *Viewer.BINDINGS,
        Binding("f", "fetch", "Fetch"),
    ]

    def __init__(
        self,
        feeds: list[Feed],
        client: httpx.AsyncClient,
        every: float = 300,
        clock: Callable[[], datetime] = local_time,
        glyph: Callable[[int], str] = GLYPHS["sextant"],
    ) -> None:
        super().__init__(site([], clock().date(), "Fetching the news..."), clock, glyph)
        self.feeds = feeds
        self.client = client
        self.every = every

    def on_mount(self) -> None:
        super().on_mount()
        self.action_fetch()
        self.set_interval(self.every, self.action_fetch)

    @work(exclusive=True)
    async def action_fetch(self) -> None:
        """Fetch every feed, in the background, and then show what arrived."""
        started = time.perf_counter()
        results = await fetch_all(self.client, self.feeds)
        took = time.perf_counter() - started
        now = self.clock()
        note = f"{len(results)} feeds in {took:.1f}s, at {now:%H:%M:%S}"
        self.site = {page.number: page for page in site(results, now.date(), note)}
        if self.number not in self.site:
            self.number = 100
        self.watch_number(self.number)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("feeds", nargs="?", type=Path, default=Path("feeds.toml"))
    parser.add_argument("--every", type=float, default=300, metavar="SECONDS")
    parser.add_argument("--glyphs", choices=sorted(GLYPHS), default="sextant")
    args = parser.parse_args()
    try:
        feeds = load_feeds(args.feeds)
    except (OSError, FeedError, ValueError) as error:
        raise SystemExit(f"Can't read the list of feeds: {error}") from error

    client = httpx.AsyncClient(timeout=10, headers=AGENT)
    Newsroom(feeds, client, args.every, glyph=GLYPHS[args.glyphs]).run()
