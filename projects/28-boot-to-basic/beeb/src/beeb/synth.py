"""Making sounds out of arithmetic. There's no Pygame in here, and no loudspeaker.

A sound is a long row of numbers, called samples, each saying where the cone of
the loudspeaker should be at one instant. This module works them out.
"""

import itertools
import math
import random
from array import array
from collections.abc import Iterator
from dataclasses import dataclass
from functools import cache

RATE = 22_050  # samples a second
LOUDEST = 32_767  # the biggest number that fits in a signed 16-bit sample


@dataclass(frozen=True)
class Envelope:
    """How a note's loudness changes over its life. Times are in seconds."""

    attack: float = 0.0  # how long it takes to reach full volume
    decay: float = 0.0  # how long it takes to fall from there to the sustain level
    sustain: float = 1.0  # the level it holds at, from 0 to 1
    release: float = 0.0  # how long it takes to die away at the end


PLAIN = Envelope(attack=0.005, release=0.01)


def frequency_of(pitch: int) -> float:
    """Convert a BBC pitch number to hertz: 53 is middle C, and 4 units are a semitone."""
    return 261.63 * 2 ** ((pitch - 53) / 48)


def square(frequency: float) -> Iterator[float]:
    """Yield a square wave, for ever: 1.0 for half of each cycle, and -1.0 for the rest."""
    period = RATE / frequency
    for n in itertools.count():
        yield 1.0 if n % period < period / 2 else -1.0


def sine(frequency: float) -> Iterator[float]:
    """Yield a sine wave, for ever: the purest tone there is."""
    step = math.tau * frequency / RATE
    for n in itertools.count():
        yield math.sin(n * step)


def noise() -> Iterator[float]:
    """Yield random samples, for ever: a hiss."""
    rng = random.Random(1)
    while True:
        yield rng.uniform(-1.0, 1.0)


def levels(envelope: Envelope, duration: float) -> Iterator[float]:
    """Yield the loudness, from 0 to 1, for every sample of a note, and then stop."""
    attack = int(envelope.attack * RATE)
    decay = int(envelope.decay * RATE)
    release = int(envelope.release * RATE)
    held = max(0, int(duration * RATE) - attack - decay)

    for n in range(attack):
        yield n / attack
    for n in range(decay):
        yield 1.0 - (1.0 - envelope.sustain) * n / decay
    for _ in range(held):
        yield envelope.sustain
    for n in range(release):
        yield envelope.sustain * (1.0 - n / release)


def samples(
    wave: Iterator[float], loudness: Iterator[float], volume: float
) -> array[int]:
    """Multiply a wave by its loudness, and pack the result as 16-bit samples."""
    top = LOUDEST * max(0.0, min(1.0, volume))
    return array("h", (int(top * w * level) for w, level in zip(wave, loudness)))


@cache
def note(
    pitch: int, duration: float, envelope: Envelope = PLAIN, volume: float = 1.0
) -> bytes:
    """Return a square-wave note, as bytes ready to be played. Pitch 0 means noise.

    Notes are remembered, so they're returned as bytes, which can't be changed.
    A remembered array could be altered by one caller, and spoilt for the rest.
    """
    wave = noise() if pitch == 0 else square(frequency_of(pitch))
    return samples(wave, levels(envelope, duration), volume).tobytes()
