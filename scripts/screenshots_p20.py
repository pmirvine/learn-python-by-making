"""Regenerate the Project 20 pictures.

uv run --project projects/20-pyfax-live --with pygame-ce python scripts/screenshots_p20.py

As with Project 19, the pages are drawn straight from the page model. The
forecast is the one that the tests use, and the letters are made up here.
"""

import json
import os
from datetime import date
from pathlib import Path

os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
from pyfax_live import letters, weather
from pyfax_live.db import Letter
from screenshots_p19 import draw

ROOT = Path(__file__).parent.parent
ASSETS = ROOT / "docs" / "assets"
P20 = ROOT / "projects" / "20-pyfax-live"
TODAY = date(2026, 9, 20)


def main() -> None:
    pygame.init()
    names = "couriernew,menlo,dejavusansmono,liberationmono"
    font = pygame.font.SysFont(names, 24, bold=True)

    london = json.loads((P20 / "tests" / "london.json").read_text(encoding="utf-8"))
    place = weather.Place("London", 51.5, -0.12)
    page = weather.page(place, weather.parse(london), TODAY)
    pygame.image.save(draw(page, font), ASSETS / "p20-weather.png")

    post = [
        Letter("Enid Parsley", "I demand a recount. That sponge was shop-bought.", ""),
        Letter("O'Brien & Sons", "Can the turtle do our car park next?", ""),
        Letter("A. Hedgehog", "No comment.", ""),
    ]
    page = letters.page(post, TODAY, "Thank you. Your letter is below.")
    pygame.image.save(draw(page, font), ASSETS / "p20-letters.png")
    print("Saved p20-weather.png and p20-letters.png")


if __name__ == "__main__":
    main()
