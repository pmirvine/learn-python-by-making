import os
import shutil
from pathlib import Path

# Tell SDL, the library underneath Pygame, not to open real windows or play
# real sound. This has to happen before pygame is imported anywhere.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pytest

from micro.computer import Micro

DISC = Path(__file__).parent.parent / "src" / "micro" / "welcome"


@pytest.fixture
def micro(tmp_path: Path) -> Micro:
    """A computer with a copy of the disc in it, which runs as fast as it can."""
    disc = tmp_path / "disc"
    shutil.copytree(DISC, disc)
    return Micro(disc, frame_rate=0)


def lines(micro: Micro) -> list[str]:
    """Return what's on the text screen, without the blank lines."""
    return [line for line in micro.screen.text().splitlines() if line.strip()]


def run(micro: Micro, *program: str, frames: int = 50) -> None:
    """Type a program in, RUN it, and give it some frames to finish in."""
    micro.type_in("NEW\n" + "".join(line + "\n" for line in program) + "RUN\n")
    for _ in range(frames):
        if not micro.running:
            break
        micro.frame()
