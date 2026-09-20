"""Ode to Joy, on channel 1, with a bass note under each bar on channel 2."""

import beeb

# BBC pitch numbers: 4 to a semitone, and 53 is middle C.
C, D, E, F, G = 53, 61, 69, 73, 81
TUNE = [E, E, F, G, G, F, E, D, C, C, D, E, E, D, D]
LENGTHS = [4] * 12 + [6, 2, 8]

beeb.mode(2)
beeb.envelope(1, attack=0.01, decay=0.08, sustain=0.5, release=0.1)

for number, (pitch, length) in enumerate(zip(TUNE, LENGTHS, strict=True)):
    beeb.sound(1, 1, pitch, length)
    if number % 4 == 0:
        beeb.sound(2, -8, pitch - 96, 16)

    beeb.gcol(0, number % 7 + 1)
    beeb.move(number * 80 + 40, 0)
    beeb.draw(number * 80 + 40, (pitch - 40) * 20)
    for _ in range(length * 50 // 20):
        beeb.vsync()
