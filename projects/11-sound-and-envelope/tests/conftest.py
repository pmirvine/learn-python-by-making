import os

# Tell SDL, the library underneath Pygame, not to open real windows or play
# real sound. This has to happen before pygame is imported anywhere.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pytest

import beeb


@pytest.fixture
def mode2():
    """A fresh MODE 2 screen for every test that asks for one."""
    beeb.mode(2)
