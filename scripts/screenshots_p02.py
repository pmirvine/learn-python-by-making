"""Regenerate the Project 2 pictures, by running each program on paper.

    uv run scripts/screenshots_p02.py

The real turtle module can't save a PNG, and screenshots are never captured by
hand, so the programs draw on tests/paperturtle.py instead.
"""

import random
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "tests"))

import paperturtle

sys.modules["turtle"] = paperturtle

P02 = ROOT / "projects" / "02-turtle-sketchbook"
ASSETS = ROOT / "docs" / "assets"

PICTURES = {
    "stages/stage1_square.py": "p02-square.png",
    "spiral.py": "p02-spiral.png",
    "stages/stage2.py": "p02-rosette.png",
    "stages/stage3.py": "p02-sky.png",
    "main.py": "p02-garden.png",
    "koch.py": "p02-koch.png",
    "solutions/seasons.py": "p02-seasons.png",
}


def main() -> None:
    for script, picture in PICTURES.items():
        paperturtle.reset()
        random.seed(2)
        runpy.run_path(str(P02 / script), run_name="__main__")
        paperturtle.save(ASSETS / picture)
        print(f"{script:24} -> docs/assets/{picture}")


if __name__ == "__main__":
    main()
