from itertools import islice, pairwise

import pytest
from waves import triangle, vibrato

from beeb.synth import RATE, Envelope, levels, samples


def test_a_triangle_wave_climbs_and_falls():
    cycle = list(islice(triangle(441), 50))
    assert cycle[0] == -1.0
    assert max(cycle) == pytest.approx(1.0, abs=0.1)
    assert cycle[:25] == sorted(cycle[:25])
    assert cycle[25:] == sorted(cycle[25:], reverse=True)


def test_vibrato_stays_in_range_and_keeps_roughly_in_tune():
    second = list(islice(vibrato(440), RATE))
    assert all(-1.0 <= sample <= 1.0 for sample in second)
    rising = sum(1 for a, b in pairwise(second) if a < 0 <= b)
    assert rising == pytest.approx(440, abs=5)


def test_any_wave_can_be_made_into_samples():
    data = samples(triangle(220), levels(Envelope(release=0.05), 0.1), volume=0.5)
    assert data.typecode == "h"
    assert len(data) == int(0.15 * RATE)
