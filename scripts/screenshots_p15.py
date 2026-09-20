"""Regenerate the Project 15 pictures.

uv run --project projects/15-sprite-editor python scripts/screenshots_p15.py
"""

import os
from pathlib import Path

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
from sprite_editor.app import SIZE, App
from sprite_editor.sprite import Sprite

ROOT = Path(__file__).parent.parent
ASSETS = ROOT / "docs" / "assets"
EXAMPLES = ROOT / "projects" / "15-sprite-editor" / "examples"


def event(kind: int, **details) -> pygame.event.Event:
    return pygame.event.Event(kind, **details)


def main() -> None:
    pygame.init()
    window = pygame.display.set_mode(SIZE)

    path = EXAMPLES / "invader.sprite"
    app = App(window, Sprite.load(path), path)
    app.draw()
    pygame.image.save(window, ASSETS / "p15-editor.png")

    # Half-way through dragging out a box, to show the preview.
    app.choose_tool(app.tools[3])
    app.choose_colour(6)
    app.handle(event(pygame.MOUSEBUTTONDOWN, button=1, pos=(16 + 25, 16 + 25)))
    app.handle(event(pygame.MOUSEMOTION, pos=(16 + 25 * 14 + 5, 16 + 25 * 14 + 5)))
    app.draw()
    pygame.image.save(window, ASSETS / "p15-box.png")

    path = EXAMPLES / "rocket.sprite"
    app = App(window, Sprite.load(path), path)
    app.draw()
    pygame.image.save(window, ASSETS / "p15-rocket.png")
    print("Saved p15-editor.png, p15-box.png and p15-rocket.png")


if __name__ == "__main__":
    main()
