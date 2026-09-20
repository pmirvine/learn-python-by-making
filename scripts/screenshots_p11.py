"""Regenerate the Project 11 pictures: the oscilloscope and the piano.

uv run --project projects/11-sound-and-envelope python scripts/screenshots_p11.py
"""

import os
import runpy
from pathlib import Path

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import beeb

ROOT = Path(__file__).parent.parent
EXAMPLES = ROOT / "projects" / "11-sound-and-envelope" / "examples"
ASSETS = ROOT / "docs" / "assets"

real_vsync = beeb.vsync


def run(script: str, frames: int, shot: str, keys: str = "") -> None:
    count = 0
    typed = list(keys)

    def vsync() -> None:
        nonlocal count
        real_vsync()
        count += 1
        if count >= frames:
            beeb.screenshot(str(ASSETS / shot))
            raise SystemExit

    beeb.vsync = vsync
    beeb.inkey = lambda: typed.pop(0) if typed else ""
    try:
        runpy.run_path(str(EXAMPLES / script), run_name="__main__")
    except SystemExit:
        print(f"{script:10} -> docs/assets/{shot}")
    finally:
        beeb.vsync = real_vsync


def main() -> None:
    run("scope.py", 2, "p11-scope.png")
    run("piano.py", 3, "p11-piano.png", keys="g")
    run("tune.py", 90, "p11-tune.png")


if __name__ == "__main__":
    main()
