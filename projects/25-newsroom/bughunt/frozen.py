"""A colleague's newsroom freezes while it fetches. "But I used async everywhere!"

    uv run bughunt/frozen.py

A heart beats ten times a second, as the app's clock would. Three feeds are
fetched "at once", and each takes a second to answer.
"""

import asyncio
import time

STARTED = time.perf_counter()


def now() -> str:
    return f"{time.perf_counter() - STARTED:4.1f}s"


def slow_download(name: str) -> str:
    """Stands in for a library that fetches a page, and doesn't return until it has."""
    time.sleep(1)
    return f"<rss>{name}</rss>"


async def fetch(name: str) -> str:
    print(f"{now()}  asking for {name}")
    page = slow_download(name)
    print(f"{now()}  {name} has arrived")
    return page


async def heart() -> None:
    while True:
        print(f"{now()}  tick")
        await asyncio.sleep(0.1)


async def main() -> None:
    beating = asyncio.create_task(heart())
    await asyncio.sleep(0.25)
    await asyncio.gather(fetch("news"), fetch("weather"), fetch("sport"))
    await asyncio.sleep(0.25)
    beating.cancel()


if __name__ == "__main__":
    asyncio.run(main())
