"""Regenerate the Project 16 pictures.

uv run --project projects/16-logo python scripts/screenshots_p16.py
"""

import importlib.util
import os
from pathlib import Path

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
from logo import Interpreter
from logo.app import SIZE, App, PygameCanvas

ROOT = Path(__file__).parent.parent
ASSETS = ROOT / "docs" / "assets"
EXAMPLES = ROOT / "projects" / "16-logo" / "examples"


def type_in(app: App, *lines: str) -> None:
    for line in lines:
        app.handle(pygame.event.Event(pygame.TEXTINPUT, text=line))
        app.handle(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))


def main() -> None:
    pygame.init()
    window = pygame.display.set_mode(SIZE)

    app = App(window)
    type_in(app, "REPEAT 4 [FD 100 RT 90]", "RT 45 SETPC 1 FD 141", "JUMP 50")
    app.draw()
    pygame.image.save(window, ASSETS / "p16-first.png")

    app = App(window)
    app.run((EXAMPLES / "tree.logo").read_text(encoding="utf-8"))
    type_in(app, "TREE 110")
    app.draw()
    pygame.image.save(window, ASSETS / "p16-tree.png")

    app = App(window)
    app.run((EXAMPLES / "spirograph.logo").read_text(encoding="utf-8"))
    type_in(app, "TO SQUARE :SIZE", "REPEAT 4 [FD :SIZE RT 90]")
    app.draw()
    pygame.image.save(window, ASSETS / "p16-spirograph.png")

    # The bug hunt: the colleague's tree, and the tree as it ought to be.
    spec = importlib.util.spec_from_file_location(
        "lopsided", ROOT / "projects" / "16-logo" / "bughunt" / "lopsided.py"
    )
    lopsided = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lopsided)
    strip = pygame.Surface((2 * 480 + 12, 480))
    strip.fill((40, 40, 40))
    for number, kind in enumerate((lopsided.ColleaguesLogo, Interpreter)):
        canvas = PygameCanvas((480, 480))
        kind(canvas).run((EXAMPLES / "tree.logo").read_text(encoding="utf-8"))
        strip.blit(canvas.surface, (number * 492, 0))
    pygame.image.save(strip, ASSETS / "p16-lopsided.png")
    print("Saved p16-first.png, p16-tree.png, p16-spirograph.png and p16-lopsided.png")


if __name__ == "__main__":
    main()
