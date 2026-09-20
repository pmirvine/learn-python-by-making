"""BBC Micro-style graphics and sound commands, built on Pygame."""

from importlib.metadata import version

from beeb.screen import (
    HEIGHT,
    WIDTH,
    canvas,
    clg,
    draw,
    gcol,
    inkey,
    mode,
    mouse,
    move,
    plot,
    point,
    screenshot,
    vsync,
)
from beeb.speaker import envelope, sound

# The one true version number is in pyproject.toml. This asks the installed package for it.
__version__ = version("beeb-lpbm")

# Everything in this list is a promise. See CHANGELOG.md for what that means.
__all__ = [
    "HEIGHT",
    "WIDTH",
    "__version__",
    "canvas",
    "clg",
    "draw",
    "envelope",
    "gcol",
    "inkey",
    "mode",
    "mouse",
    "move",
    "plot",
    "point",
    "screenshot",
    "sound",
    "vsync",
]
