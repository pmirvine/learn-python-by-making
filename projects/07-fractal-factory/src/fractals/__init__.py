"""Fractal Factory: pictures from formulas."""

from fractals.fields import Field, escape_time, julia, mandelbrot, plasma
from fractals.palettes import (
    PALETTES,
    Colour,
    Palette,
    black_inside,
    cycled,
    gradient,
    steps,
)
from fractals.render import render

__all__ = [
    "PALETTES",
    "Colour",
    "Field",
    "Palette",
    "black_inside",
    "cycled",
    "escape_time",
    "gradient",
    "julia",
    "mandelbrot",
    "plasma",
    "render",
    "steps",
]
