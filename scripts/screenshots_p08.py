"""Regenerate the Project 8 screenshots without opening a window.

Run from the repository root, inside the project's environment:

    uv run --project projects/08-mode2-sketchpad python scripts/screenshots_p08.py
"""

import math
import os
import random
import runpy
from pathlib import Path

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import beeb
import pygame

ROOT = Path(__file__).parent.parent
EXAMPLES = ROOT / "projects" / "08-mode2-sketchpad" / "examples"
ASSETS = ROOT / "docs" / "assets"

real_vsync = beeb.vsync
real_flip = pygame.display.flip


def run(script: str, frames: int, shot: str, *, raw: bool = False) -> None:
    """Run an example for a number of frames, save what's on screen, then stop it.

    An empty script name means the package's own test card, `uv run beeb`.
    """
    count = 0

    def finish_after_enough_frames() -> None:
        nonlocal count
        count += 1
        if count < frames:
            return
        if raw:
            pygame.image.save(pygame.display.get_surface(), ASSETS / shot)
        else:
            beeb.screenshot(str(ASSETS / shot))
        raise SystemExit

    def vsync() -> None:
        real_vsync()
        finish_after_enough_frames()

    def flip() -> None:
        real_flip()
        finish_after_enough_frames()

    beeb.vsync = vsync
    pygame.display.flip = real_flip if not raw else flip
    random.seed(8)
    try:
        if script:
            runpy.run_path(str(EXAMPLES / script), run_name="__main__")
        else:
            beeb.main()
    except SystemExit:
        print(f"{script or 'test card':14} -> docs/assets/{shot}")
    finally:
        beeb.vsync = real_vsync
        pygame.display.flip = real_flip


def scripted_painting() -> None:
    """Drive paint.py with a fake mouse and keyboard, to paint a little scene."""
    strokes: list[tuple[str, list[tuple[int, int]]]] = [
        ("3", [(1000 + int(90 * math.cos(a / 5)), 800 + int(90 * math.sin(a / 5))) for a in range(33)]),
        ("2", [(x, 250 + int(60 * math.sin(x / 90))) for x in range(0, 1280, 16)]),
        ("1", [(300, 280), (300, 560), (620, 560), (620, 280)]),
        ("5", [(260, 560), (460, 760), (660, 560)]),
        ("6", [(x, 900 + int(40 * math.sin(x / 40))) for x in range(80, 700, 16)]),
    ]
    events: list[tuple[str, tuple[int, int], bool]] = []
    for key, points in strokes:
        events.append((key, points[0], False))
        events.extend(("", p, True) for p in points)
        events.append(("", points[-1], False))

    playback = iter(events)
    current = ("", (0, 0), False)

    def inkey() -> str:
        nonlocal current
        current = next(playback, ("", (0, 0), False))
        return current[0]

    def mouse() -> tuple[int, int, tuple[bool, bool, bool]]:
        return (*current[1], (current[2], False, False))

    real_inkey, real_mouse = beeb.inkey, beeb.mouse
    beeb.inkey, beeb.mouse = inkey, mouse
    try:
        run("paint.py", len(events) + 2, "p08-paint.png")
    finally:
        beeb.inkey, beeb.mouse = real_inkey, real_mouse


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    run("window.py", 60, "p08-window.png", raw=True)
    run("moire_raw.py", 2, "p08-moire-raw.png", raw=True)
    run("moire.py", 90, "p08-moire.png")
    run("lines.py", 200, "p08-lines.png")
    run("strings.py", 1, "p08-strings.png")
    scripted_painting()
    run("", 2, "p08-testcard.png")


if __name__ == "__main__":
    main()
