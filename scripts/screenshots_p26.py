"""Regenerate the Project 26 pictures.

uv run --project projects/26-adventure-third-edition python scripts/screenshots_p26.py
"""

import asyncio
from pathlib import Path

from adventure.app import AdventureApp
from adventure.colossal import Colossal
from textual.widgets import Input

ROOT = Path(__file__).parent.parent
ASSETS = ROOT / "docs" / "assets"
EXPLORING = ["south", "east", "take torch", "south", "examine flowerpots", "take key"]
REST = ["n", "w", "unlock door", "w", "take cassette", "e", "u", "u", "load cassette"]
WINNING = EXPLORING + REST


async def shoot(
    name: str, commands: list[str], size: tuple[int, int] = (90, 28)
) -> None:
    app = AdventureApp(Colossal)
    async with app.run_test(size=size) as pilot:
        for command in commands:
            app.query_one(Input).value = command
            await pilot.press("enter")
        await pilot.pause()
        svg = app.export_screenshot(title="uv run adventure")
    (ASSETS / name).write_text(svg, encoding="utf-8")


def main() -> None:
    asyncio.run(shoot("p26-exploring.svg", EXPLORING))
    asyncio.run(shoot("p26-the-end.svg", WINNING))
    print("Saved p26-exploring.svg and p26-the-end.svg")


if __name__ == "__main__":
    main()
