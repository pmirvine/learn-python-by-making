"""Regenerate the Project 14 pictures.

uv run --project projects/14-wireframe python scripts/screenshots_p14.py
"""

import os
from pathlib import Path

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
from wireframe.app import SIZE, App
from wireframe.matrix import rotation_x, rotation_y
from wireframe.model import hangar, load
from wireframe.view import Style

ROOT = Path(__file__).parent.parent
ASSETS = ROOT / "docs" / "assets"
P14 = ROOT / "projects" / "14-wireframe"
STILL = (0.0, 0.0, 0.0)


def snap(window: pygame.Surface) -> pygame.Surface:
    """Return the little window, three times the size, as it looks on the screen."""
    return pygame.transform.scale_by(window, 3)


def side_by_side(pictures: list[pygame.Surface]) -> pygame.Surface:
    width = sum(picture.get_width() for picture in pictures) + 12 * (len(pictures) - 1)
    strip = pygame.Surface((width, pictures[0].get_height()))
    strip.fill((40, 40, 40))
    x = 0
    for picture in pictures:
        strip.blit(picture, (x, 0))
        x += picture.get_width() + 12
    return strip


def main() -> None:
    pygame.init()
    window = pygame.display.set_mode(SIZE)
    app = App(window, hangar())
    app.drifting = False
    names = [ship.name for ship in app.ships]

    app.show(names.index("Manta"))
    app.orientation = rotation_x(25) @ rotation_y(-35)
    app.frame(0.0, STILL)
    pygame.image.save(snap(window), ASSETS / "p14-manta.png")

    pictures = []
    for style in Style:
        app.style = style
        app.frame(0.0, STILL)
        pictures.append(window.copy())
    pygame.image.save(
        pygame.transform.scale_by(side_by_side(pictures), 2), ASSETS / "p14-styles.png"
    )

    pictures = []
    app.style = Style.SOLID
    for name in names:
        app.show(names.index(name))
        app.frame(0.0, STILL)
        pictures.append(window.copy())
    pygame.image.save(side_by_side(pictures), ASSETS / "p14-hangar.png")

    pictures = []
    for path in (P14 / "bughunt" / "skiff.toml", P14 / "solutions/bughunt/skiff.toml"):
        app.ships.append(load(path))
        app.show(len(app.ships) - 1)
        app.orientation = rotation_x(35) @ rotation_y(-40)
        for style in (Style.HIDDEN, Style.SOLID):
            app.style = style
            app.frame(0.0, STILL)
            pictures.append(window.copy())
    pygame.image.save(side_by_side(pictures), ASSETS / "p14-skiff.png")
    print("Saved p14-manta.png, p14-styles.png, p14-hangar.png and p14-skiff.png")


if __name__ == "__main__":
    main()
