"""BBC Micro-style sound commands: SOUND and ENVELOPE, more or less.

The arithmetic is in beeb.synth. This module owns the loudspeaker.
"""

import pygame

from beeb.synth import PLAIN, RATE, Envelope, note

CHANNELS = 4  # channel 0 is the noise channel, and 1 to 3 play tones


class Speaker:
    """Pygame's mixer, with four channels and some numbered envelopes."""

    FORMAT = (RATE, -16, 1)  # samples a second, signed 16-bit, one channel (mono)

    def __init__(self) -> None:
        # pygame.init() may have opened the mixer already, in some other format,
        # in which case our samples would come out at the wrong speed and pitch.
        if pygame.mixer.get_init() != self.FORMAT:
            pygame.mixer.quit()
            pygame.mixer.init(*self.FORMAT, allowedchanges=0)
        self.channels = [pygame.mixer.Channel(n) for n in range(CHANNELS)]
        self.envelopes: dict[int, Envelope] = {}

    def envelope(self, number: int, envelope: Envelope) -> None:
        self.envelopes[number] = envelope

    def sound(self, channel: int, amplitude: int, pitch: int, duration: int) -> None:
        if not 0 <= channel < CHANNELS:
            raise ValueError(
                f"There are channels 0 to {CHANNELS - 1}, and no channel {channel}"
            )
        if amplitude > 0:
            shape, volume = self.envelopes.get(amplitude, PLAIN), 1.0
        else:
            shape, volume = PLAIN, min(-amplitude, 15) / 15
        if channel == 0:
            pitch = 0
        data = note(pitch, duration / 20, shape, volume)
        self.channels[channel].play(pygame.mixer.Sound(buffer=data))


_speaker: Speaker | None = None


def _the_speaker() -> Speaker:
    """Return the one Speaker, switching it on the first time it's wanted."""
    global _speaker
    if _speaker is None:
        _speaker = Speaker()
    return _speaker


def sound(channel: int, amplitude: int, pitch: int, duration: int) -> None:
    """Play a note: SOUND channel, amplitude, pitch, duration.

    amplitude is 0 (silent) down to -15 (loudest), or 1 to 4 to use an envelope.
    pitch is in quarters of a semitone, and 53 is middle C. duration is in
    twentieths of a second. A new note on a channel cuts off the one before.
    """
    _the_speaker().sound(channel, amplitude, pitch, duration)


def envelope(
    number: int,
    attack: float = 0.0,
    decay: float = 0.0,
    sustain: float = 1.0,
    release: float = 0.0,
) -> None:
    """Define envelope 1, 2, 3 or 4, for SOUND to use in place of an amplitude."""
    if not 1 <= number <= 4:
        raise ValueError("Envelopes are numbered from 1 to 4")
    _the_speaker().envelope(number, Envelope(attack, decay, sustain, release))
