import os
import shutil
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from touch import install_touch

from micro.computer import Micro

DISC = Path(__file__).parent.parent / "src" / "micro" / "welcome"
PROGRAM = [
    "10 MODE 1: GCOL 0,2: MOVE 0,100: DRAW 1279,100",
    '20 SPRITE 1,"ship"',
    "30 PUT 1,600,400: PRINT TOUCH(1);",
    "40 PUT 1,600,90: PRINT TOUCH(1);",
    "50 PUT 1,600,104: PRINT TOUCH(1)",
]


def test_a_sprite_lands_on_a_line(tmp_path: Path):
    micro = Micro(Path(shutil.copytree(DISC, tmp_path / "disc")), frame_rate=0)
    install_touch(micro)
    micro.type_in("".join(line + "\n" for line in PROGRAM) + "RUN\n")
    while micro.running:
        micro.frame()
    assert micro.screen.text().splitlines()[0] == "0-10"
