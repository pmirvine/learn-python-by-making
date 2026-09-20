"""Run a Pygame program for a few frames without opening a window, then stop it.

    python tests/headless.py path/to/program.py 10

Exits with status 0 if the program reached that many frames. If the program
crashes first, the traceback and a non-zero status come through as usual.
"""

import os
import runpy
import sys
from pathlib import Path

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame


def main() -> None:
    script = Path(sys.argv[1]).resolve()
    frames = int(sys.argv[2])
    real_flip = pygame.display.flip
    count = 0

    def flip() -> None:
        nonlocal count
        real_flip()
        count += 1
        if count >= frames:
            raise SystemExit(0)

    pygame.display.flip = flip
    # Python puts a script's own folder first on the import path; do the same.
    sys.path.insert(0, str(script.parent))
    runpy.run_path(str(script), run_name="__main__")
    raise SystemExit(f"{script.name} finished before drawing {frames} frames")


if __name__ == "__main__":
    main()
