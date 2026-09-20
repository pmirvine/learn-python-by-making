"""The failing test for the colleague's unpack, and the same test for the real one."""

import importlib.util
from pathlib import Path

import pytest

from pyfax import mosaic


def colleagues_unpack():
    path = Path(__file__).parent.parent.parent / "bughunt" / "dotty.py"
    spec = importlib.util.spec_from_file_location("dotty", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.unpack


@pytest.mark.parametrize("dots", range(64))
def test_what_is_packed_can_be_unpacked(dots):
    assert mosaic.pack(mosaic.unpack(dots)) == [[dots]]


def test_the_colleagues_version_only_ever_sees_the_first_square():
    unpack = colleagues_unpack()
    wrong = [dots for dots in range(64) if mosaic.pack(unpack(dots)) != [[dots]]]
    assert len(wrong) == 62
    assert {tuple(unpack(dots)) for dots in range(64)} == {
        ("..", "..", ".."),
        ("#.", "..", ".."),
    }
