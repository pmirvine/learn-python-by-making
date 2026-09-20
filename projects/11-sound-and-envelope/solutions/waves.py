"""The Extend challenges: a triangle wave, and a note with vibrato.

These import from the installed `beeb` package, as any other project would.
"""

import itertools
import math
from collections.abc import Iterator

from beeb.synth import RATE


def triangle(frequency: float) -> Iterator[float]:
    """Yield a triangle wave, for ever: softer than a square, brighter than a sine."""
    period = RATE / frequency
    for n in itertools.count():
        position = n % period / period
        yield 4 * position - 1 if position < 0.5 else 3 - 4 * position


def vibrato(
    frequency: float, depth: float = 0.02, speed: float = 6.0
) -> Iterator[float]:
    """Yield a sine wave whose pitch wobbles, `speed` times a second.

    The frequency keeps changing, so `n * step` won't do. The wave has to
    remember how far round the circle it has got, and move on from there.
    """
    phase = 0.0
    for n in itertools.count():
        wobble = math.sin(math.tau * speed * n / RATE)
        phase += math.tau * frequency * (1 + depth * wobble) / RATE
        yield math.sin(phase)
