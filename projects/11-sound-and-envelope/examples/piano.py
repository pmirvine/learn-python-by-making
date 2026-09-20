"""A piano. The keys A S D F G H J K are the white notes, from middle C up to C.

W E T Y U are the black notes, where a real piano has them. 1 to 4 choose an
envelope, and the space bar is a drum. Escape quits.
"""

import beeb

WHITE = {"a": 53, "s": 61, "d": 69, "f": 73, "g": 81, "h": 89, "j": 97, "k": 101}
BLACK = {"w": 57, "e": 65, "t": 77, "y": 85, "u": 93}
KEY_WIDTH = beeb.WIDTH // len(WHITE)


def draw_keyboard(pressed: str) -> None:
    """Draw the white keys as outlines, with the one that's pressed filled in."""
    beeb.clg()
    for number, key in enumerate(WHITE):
        left, right = number * KEY_WIDTH + 8, (number + 1) * KEY_WIDTH - 8
        beeb.gcol(0, 3 if key == pressed else 7)
        if key == pressed:
            beeb.move(left, 200)
            beeb.move(right, 200)
            beeb.plot(85, left, 800)
            beeb.plot(85, right, 800)
        else:
            beeb.move(left, 200)
            beeb.draw(right, 200)
            beeb.draw(right, 800)
            beeb.draw(left, 800)
            beeb.draw(left, 200)


def main() -> None:
    beeb.mode(1)
    beeb.envelope(1, attack=0.005, decay=0.1, sustain=0.6, release=0.15)
    beeb.envelope(2, attack=0.2, decay=0.0, sustain=1.0, release=0.4)
    beeb.envelope(3, attack=0.0, decay=0.15, sustain=0.0, release=0.0)
    beeb.envelope(4, attack=0.0, decay=0.05, sustain=0.2, release=0.6)
    shape = 1
    pressed = ""
    channel = 1

    while True:
        key = beeb.inkey().lower()
        if key in WHITE or key in BLACK:
            pitch = WHITE.get(key) or BLACK[key]
            beeb.sound(channel, shape, pitch, 8)
            channel = channel % 3 + 1
            pressed = key
        elif key == " ":
            beeb.sound(0, 3, 0, 4)
        elif key.isdigit() and 1 <= int(key) <= 4:
            shape = int(key)
        draw_keyboard(pressed)
        beeb.vsync()


if __name__ == "__main__":
    main()
