"""Conway's Game of Life."""

from life.core import Cell, generations, neighbours, normalise, period, step
from life.patterns import PATTERNS, parse, shift, soup
from life.render import render

__all__ = [
    "PATTERNS",
    "Cell",
    "generations",
    "neighbours",
    "normalise",
    "parse",
    "period",
    "render",
    "shift",
    "soup",
    "step",
]
