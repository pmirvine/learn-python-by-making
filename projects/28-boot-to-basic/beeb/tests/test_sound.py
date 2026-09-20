import pygame
import pytest

import beeb
from beeb import speaker


def test_sound_plays_on_the_channel_it_is_given():
    beeb.sound(1, -15, 53, 20)
    assert pygame.mixer.Channel(1).get_busy()
    assert not pygame.mixer.Channel(3).get_busy()


def test_a_new_note_replaces_the_old_one_on_the_same_channel():
    beeb.sound(2, -15, 53, 40)
    first = pygame.mixer.Channel(2).get_sound()
    beeb.sound(2, -15, 101, 40)
    assert pygame.mixer.Channel(2).get_sound() is not first


def test_channel_nought_is_noise_whatever_the_pitch():
    beeb.sound(0, -10, 200, 2)
    assert pygame.mixer.Channel(0).get_busy()


def test_there_are_four_channels():
    with pytest.raises(ValueError, match="no channel 4"):
        beeb.sound(4, -15, 53, 1)


def test_envelopes_are_numbered_one_to_four():
    beeb.envelope(4, attack=0.1)
    with pytest.raises(ValueError, match="from 1 to 4"):
        beeb.envelope(5, attack=0.1)


def test_a_positive_amplitude_means_an_envelope():
    beeb.envelope(2, attack=0.0, decay=0.0, sustain=1.0, release=0.5)
    beeb.sound(3, 2, 53, 10)
    long_note = pygame.mixer.Channel(3).get_sound().get_length()
    beeb.sound(3, -15, 53, 10)
    short_note = pygame.mixer.Channel(3).get_sound().get_length()
    assert long_note == pytest.approx(1.0, abs=0.01)
    assert short_note == pytest.approx(0.51, abs=0.01)


def test_the_mixer_is_in_our_format_even_if_pygame_got_there_first():
    pygame.mixer.quit()
    pygame.mixer.init(44_100, -16, 2)
    speaker._speaker = None
    beeb.sound(1, -15, 53, 10)
    assert pygame.mixer.get_init() == (22_050, -16, 1)
    assert pygame.mixer.Channel(1).get_sound().get_length() == pytest.approx(
        0.51, abs=0.01
    )


def test_there_is_only_ever_one_speaker():
    beeb.sound(1, -5, 53, 1)
    assert speaker._the_speaker() is speaker._the_speaker()
