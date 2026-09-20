"""Regenerate the Pyxel side quest's picture, with the real Pyxel.

uv run --project projects/15x-pyxel-side-quest python scripts/screenshots_p15x.py

Pyxel needs OpenGL, and so, unlike the other screenshot scripts, this one opens
a real window for a moment, and can't run on a machine with no display.
"""

import runpy
from pathlib import Path

import pyxel

ROOT = Path(__file__).parent.parent
GAME = ROOT / "projects" / "15x-pyxel-side-quest" / "meteors.py"
FRAMES = 400


def run_for_a_while(update, draw) -> None:
    """Stand in for pyxel.run: dodge until there's something worth a picture."""
    game = update.__self__
    real_btn = pyxel.btn
    for _ in range(FRAMES):
        threats = [
            meteor
            for meteor in game.meteors
            if abs(meteor[0] - game.x - 8) < 14 and 40 < meteor[1] < 124
        ]
        steer = None
        if threats:
            nearest = max(threats, key=lambda meteor: meteor[1])
            steer = pyxel.KEY_RIGHT if nearest[0] < game.x + 8 else pyxel.KEY_LEFT
        pyxel.btn = lambda key, steer=steer: key == steer
        update()
        draw()
        pyxel.flip()
        if game.alive and game.score >= 12 and len(game.meteors) >= 6:
            break
    pyxel.btn = real_btn
    pyxel.screen.save(str(ROOT / "docs" / "assets" / "p15x-meteors"), 4)
    print(f"Saved p15x-meteors.png (alive: {game.alive}, score: {game.score})")


def main() -> None:
    pyxel.run = run_for_a_while
    pyxel.rseed(15)
    runpy.run_path(str(GAME))


if __name__ == "__main__":
    main()
