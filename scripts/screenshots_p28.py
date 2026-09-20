"""Regenerate the Project 28 pictures, by typing at the computer, with no window.

uv run --project projects/28-boot-to-basic python scripts/screenshots_p28.py
"""

import os
import shutil
import tempfile
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import runpy

import pygame
from micro.computer import Micro

ROOT = Path(__file__).parent.parent
ASSETS = ROOT / "docs" / "assets"
DISC = ROOT / "projects" / "28-boot-to-basic" / "src" / "micro" / "welcome"
HELLO = [
    '10 PRINT "HELLO FROM ";',
    '20 PRINT "A COMPUTER THAT I MADE"',
    "30 SOUND 1,-15,53,10",
    "LIST",
    "RUN",
]


def save(name: str) -> None:
    window = pygame.display.get_surface()
    assert window is not None
    pygame.image.save(window, ASSETS / name)


def main() -> None:
    stage3 = ROOT / "projects" / "28-boot-to-basic" / "stages" / "stage3_screen.py"
    runpy.run_path(str(stage3))["main"](frames=1)
    save("p28-layers.png")

    with tempfile.TemporaryDirectory() as folder:
        disc = Path(shutil.copytree(DISC, Path(folder) / "disc"))
        micro = Micro(disc, frame_rate=0)
        micro.frame()
        save("p28-boot.png")

        micro.type_in("".join(line + "\n" for line in HELLO))
        for _ in range(5):
            micro.frame()
        micro.frames = 0  # so that the cursor is showing
        micro.frame()
        save("p28-hello.png")

        micro.type_in('LOAD "carpet"\nRUN\n')
        while micro.running:
            micro.frame()
        micro.screen.clear()
        micro.frames = 16  # and so that here it isn't
        micro.frame()
        save("p28-carpet.png")

        micro.type_in('LOAD "alien"\nRUN\n')
        micro.press(pygame.K_RETURN)
        for _ in range(3000):
            micro.frame()
            basic = micro.machine.variables
            if basic.get("S", 0) >= 10 and basic["F"] and basic["BY"] > 400:
                break
        save("p28-alien.png")
    print("Saved p28-layers, p28-boot, p28-hello, p28-carpet and p28-alien (.png)")


if __name__ == "__main__":
    main()
