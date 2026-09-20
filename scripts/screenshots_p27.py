"""Regenerate the Project 27 picture: the test card, which also goes in beeb's README.

uv run --project projects/27-ship-it python scripts/screenshots_p27.py
"""

import os
import shutil
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import beeb
from beeb import cli

ROOT = Path(__file__).parent.parent
ASSET = ROOT / "docs" / "assets" / "p27-testcard.png"
IN_README = ROOT / "projects" / "27-ship-it" / "docs" / "testcard.png"


def main() -> None:
    cli.test_card()
    beeb.screenshot(str(ASSET))
    shutil.copyfile(ASSET, IN_README)
    print(f"Saved {ASSET.name}, and a copy for the README")


if __name__ == "__main__":
    main()
