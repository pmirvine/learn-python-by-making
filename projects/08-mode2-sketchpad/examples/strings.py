import math

import beeb

POINTS = 150
RADIUS = 500

beeb.mode(1)
times = 2.0
while True:
    beeb.clg()
    beeb.gcol(0, int(times) % 3 + 1)
    for i in range(POINTS):
        a = math.tau * i / POINTS
        b = a * times
        beeb.move(640 + RADIUS * math.cos(a), 512 + RADIUS * math.sin(a))
        beeb.draw(640 + RADIUS * math.cos(b), 512 + RADIUS * math.sin(b))
    times += 0.005
    beeb.vsync()
