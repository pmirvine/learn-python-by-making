"""Regenerate the Project 19 pictures.

uv run --project projects/19-pyfax --with pygame-ce python scripts/screenshots_p19.py

There's no browser to hand when the tutorial is checked, so this draws each page
straight from the page model, a cell at a time, as the stylesheet would.
"""

import os
from datetime import date
from pathlib import Path

os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
from pyfax.content import pages
from pyfax.page import COLUMNS, ROWS, Page

ROOT = Path(__file__).parent.parent
ASSETS = ROOT / "docs" / "assets"
CONTENT = ROOT / "projects" / "19-pyfax" / "content"
CELL = (24, 30)


def rgb(css: str) -> tuple[int, int, int]:
    red, green, blue = (255 if digit == "f" else 0 for digit in css[1:])
    return red, green, blue


def draw(page: Page, font: pygame.font.Font) -> pygame.Surface:
    width, height = CELL
    picture = pygame.Surface((COLUMNS * width, ROWS * height))
    for y, row in enumerate(page.rows):
        for x, cell in enumerate(row):
            box = pygame.Rect(x * width, y * height, width, height)
            picture.fill(rgb(cell.paper.css), box)
            if cell.dots:
                for position in range(6):
                    if cell.dots >> position & 1:
                        dot = pygame.Rect(
                            box.left + position % 2 * width // 2,
                            box.top + position // 2 * height // 3,
                            width // 2,
                            height // 3,
                        )
                        picture.fill(rgb(cell.ink.css), dot)
            elif cell.text != " ":
                glyph = font.render(cell.text, True, rgb(cell.ink.css))
                picture.blit(glyph, glyph.get_rect(center=box.center))
    return picture


def main() -> None:
    pygame.init()
    names = "couriernew,menlo,dejavusansmono,liberationmono"
    font = pygame.font.SysFont(names, 24, bold=True)
    site = {page.number: page for page in pages(CONTENT, date(2026, 9, 20))}
    for number in (100, 101, 301, 501):
        pygame.image.save(draw(site[number], font), ASSETS / f"p19-page{number}.png")
    print("Saved p19-page100.png, p19-page101.png, p19-page301.png and p19-page501.png")


if __name__ == "__main__":
    main()
