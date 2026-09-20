from array import array
from itertools import islice

import pytest

from beeb.synth import (
    LOUDEST,
    RATE,
    Envelope,
    frequency_of,
    levels,
    noise,
    note,
    samples,
    sine,
    square,
)


@pytest.mark.parametrize(
    ("pitch", "hertz"),
    [(53, 261.63), (89, 440.0), (101, 523.25), (5, 130.81), (149, 1046.5)],
)
def test_pitch_numbers_are_quarter_semitones_from_middle_c(pitch, hertz):
    assert frequency_of(pitch) == pytest.approx(hertz, rel=0.001)


def test_a_square_wave_spends_half_its_time_at_each_level():
    second = list(islice(square(441), RATE))
    assert set(second) == {1.0, -1.0}
    assert second.count(1.0) == pytest.approx(RATE / 2, abs=50)
    assert second[:25] == [1.0] * 25
    assert second[25:50] == [-1.0] * 25


def test_a_sine_wave_starts_at_nought_and_stays_in_range():
    cycle = list(islice(sine(441), 50))
    assert cycle[0] == 0.0
    assert max(cycle) == pytest.approx(1.0, abs=0.01)
    assert min(cycle) == pytest.approx(-1.0, abs=0.01)


def test_noise_is_the_same_hiss_every_time():
    assert list(islice(noise(), 100)) == list(islice(noise(), 100))
    assert all(-1.0 <= sample <= 1.0 for sample in islice(noise(), 1000))


def test_a_plain_envelope_is_full_volume_all_the_way():
    loudness = list(levels(Envelope(), duration=0.01))
    assert len(loudness) == 220
    assert set(loudness) == {1.0}


def test_an_envelope_rises_falls_holds_and_dies_away():
    shape = Envelope(attack=0.1, decay=0.1, sustain=0.5, release=0.1)
    loudness = list(levels(shape, duration=0.4))
    tenth = RATE // 10

    assert len(loudness) == 5 * tenth
    assert loudness[0] == 0.0
    assert loudness[tenth] == 1.0
    assert loudness[2 * tenth] == 0.5
    assert loudness[3 * tenth] == 0.5
    assert loudness[-1] == pytest.approx(0.0, abs=0.001)
    assert loudness[:tenth] == sorted(loudness[:tenth])


def test_samples_are_sixteen_bit_and_never_too_loud():
    data = samples(square(440), levels(Envelope(), 0.01), volume=1.0)
    assert data.typecode == "h"
    assert data.itemsize == 2
    assert set(data) == {LOUDEST, -LOUDEST}
    assert len(data.tobytes()) == 2 * len(data)


def test_volume_scales_the_samples():
    quiet = samples(square(440), levels(Envelope(), 0.01), volume=0.5)
    assert max(quiet) == LOUDEST // 2
    silent = samples(square(440), levels(Envelope(), 0.01), volume=0.0)
    assert set(silent) == {0}


def test_a_note_lasts_as_long_as_it_is_told_plus_its_release():
    shape = Envelope(release=0.1)
    assert len(note(53, 0.5, shape)) == 2 * (RATE // 2 + RATE // 10)


def test_notes_are_remembered():
    shape = Envelope(attack=0.01, decay=0.02, sustain=0.3, release=0.04)
    assert note(77, 0.2, shape) is note(77, 0.2, shape)
    assert note(77, 0.2, shape) is not note(81, 0.2, shape)


def test_pitch_nought_is_noise():
    hiss = array("h", note(0, 0.05, Envelope()))
    assert len(set(hiss)) > 100


def test_a_remembered_note_cannot_be_spoilt():
    data = note(53, 0.1)
    assert isinstance(data, bytes)
    with pytest.raises(TypeError):
        data[0] = 0
