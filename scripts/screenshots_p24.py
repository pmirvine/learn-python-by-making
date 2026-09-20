"""Regenerate the Project 24 pictures, which are SVGs that Textual writes itself.

uv run --project projects/24-teletext-viewer python scripts/screenshots_p24.py
"""

import asyncio
from datetime import UTC, date, datetime
from pathlib import Path

from pyfax.content import pages
from teleview.app import Viewer
from teleview.glyphs import quadrant

ROOT = Path(__file__).parent.parent
ASSETS = ROOT / "docs" / "assets"
CONTENT = ROOT / "projects" / "24-teletext-viewer" / "content"
NOON = datetime(2026, 9, 20, 12, 0, 0, tzinfo=UTC)


async def shoot(name: str, *keys: str) -> None:
    # Quadrants, since the font that the picture is drawn in has no sextants.
    site = pages(CONTENT, date(2026, 9, 20))
    app = Viewer(site, clock=lambda: NOON, glyph=quadrant)
    async with app.run_test(size=(60, 30)) as pilot:
        await pilot.press(*keys)
        await pilot.pause()
        svg = app.export_screenshot(title="uv run teleview")
    (ASSETS / name).write_text(svg, encoding="utf-8")


def main() -> None:
    asyncio.run(shoot("p24-index.svg"))
    asyncio.run(shoot("p24-weather.svg", "3", "0", "1"))
    print("Saved p24-index.svg and p24-weather.svg")


if __name__ == "__main__":
    main()
