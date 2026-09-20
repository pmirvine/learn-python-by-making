"""Three notes at once, mixed into one sound. It works for quiet notes, and crashes for loud ones."""

from array import array

import pygame

from beeb.synth import RATE, Envelope, note

ORGAN = Envelope(attack=0.05, release=0.3)


def mix(*notes: array) -> array:
    """Add several notes together, sample by sample, into one."""
    return array("h", (sum(group) for group in zip(*notes, strict=True)))


def chord(pitches: list[int], duration: float, volume: float) -> array:
    """Return one sound made of all the pitches, played together."""
    return mix(*(array("h", note(pitch, duration, ORGAN, volume)) for pitch in pitches))


def main() -> None:
    pygame.mixer.init(RATE, -16, 1, allowedchanges=0)
    c_major = [53, 69, 81]

    print("Quietly...")
    pygame.mixer.Sound(buffer=chord(c_major, 1.0, volume=0.3)).play()
    pygame.time.wait(1500)

    print("And now loudly...")
    pygame.mixer.Sound(buffer=chord(c_major, 1.0, volume=0.9)).play()
    pygame.time.wait(1500)


if __name__ == "__main__":
    main()
