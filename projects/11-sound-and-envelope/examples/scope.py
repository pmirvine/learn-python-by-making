"""An oscilloscope: see the shape of the note that you're hearing."""

import beeb
from beeb.synth import LOUDEST, Envelope, levels, samples, square

SHAPE = Envelope(attack=0.05, decay=0.1, sustain=0.4, release=0.2)

beeb.mode(0)
beeb.envelope(1, SHAPE.attack, SHAPE.decay, SHAPE.sustain, SHAPE.release)
beeb.sound(1, 1, 5, 10)

data = samples(square(130.81), levels(SHAPE, 0.5), volume=1.0)
beeb.move(0, 512)
for x in range(0, beeb.WIDTH, 2):
    sample = data[x * len(data) // beeb.WIDTH]
    beeb.draw(x, 512 + 480 * sample / LOUDEST)

while True:
    beeb.vsync()
