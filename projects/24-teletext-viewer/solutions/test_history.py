import asyncio
from datetime import date
from pathlib import Path

from history import ViewerWithBack
from pyfax.content import pages

CONTENT = Path(__file__).parent.parent / "content"


def numbers_after(*keys: str) -> list[int]:
    """Press the keys one at a time, and note the page after each whole move."""

    async def scenario() -> list[int]:
        app = ViewerWithBack(pages(CONTENT, date(2026, 9, 20)))
        seen: list[int] = []
        async with app.run_test(size=(60, 30)) as pilot:
            for key in keys:
                await pilot.press(key)
                await pilot.pause()
                seen.append(app.number)
        return seen

    return asyncio.run(scenario())


def test_backspace_goes_back_the_way_you_came():
    seen = numbers_after(
        "3", "0", "1", "5", "0", "1", "backspace", "backspace", "backspace"
    )
    assert seen == [100, 100, 301, 301, 301, 501, 301, 100, 100]
