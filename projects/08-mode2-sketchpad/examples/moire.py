import beeb

beeb.mode(1)
for x in range(0, 1280, 16):
    beeb.gcol(0, 1)
    beeb.move(0, 0)
    beeb.draw(x, 1023)
    beeb.gcol(0, 2)
    beeb.move(1279, 0)
    beeb.draw(1279 - x, 1023)
    beeb.vsync()

while True:
    beeb.vsync()
