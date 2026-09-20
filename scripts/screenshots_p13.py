"""Regenerate the Project 13 pictures.

uv run --project projects/13-life-in-pixels python scripts/screenshots_p13.py
"""

import os
from pathlib import Path

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
from life import PATTERNS, parse, soup
from pixel_life.app import App

ASSETS = Path(__file__).parent.parent / "docs" / "assets"


def main() -> None:
    pygame.init()
    window = pygame.display.set_mode((960, 720))
    app = App(window)

    for _ in range(140):
        app.simulation.step()
    app.message = "The glider gun, after 140 generations."
    app.frame(0.0)
    pygame.image.save(window, ASSETS / "p13-gun.png")

    app.simulation.load(soup(480, 360, seed=13))
    for _ in range(60):
        app.simulation.step()
    app.camera.x = app.camera.y = 0.0
    app.camera.zoom = 2.0
    app.message = "Random soup, sixty generations on, zoomed right out."
    app.frame(0.0)
    pygame.image.save(window, ASSETS / "p13-soup.png")

    app.load_pattern(parse(PATTERNS["acorn"]), "acorn")
    app.camera.zoom_about((480, 360), 4)
    app.frame(0.0)
    pygame.image.save(window, ASSETS / "p13-acorn.png")
    print("Saved p13-gun.png, p13-soup.png and p13-acorn.png")


if __name__ == "__main__":
    main()
