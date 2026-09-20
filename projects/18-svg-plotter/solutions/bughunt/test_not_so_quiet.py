"""The failing test for the colleague's plotter, and the same test for yours."""

import importlib.util
from pathlib import Path

import pytest

from plotter import Plot


def colleagues_plot() -> type[Plot]:
    path = Path(__file__).parent.parent.parent / "bughunt" / "quiet.py"
    spec = importlib.util.spec_from_file_location("quiet", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.QuietPlot


def test_a_mistake_inside_the_with_is_not_kept_quiet(tmp_path):
    with pytest.raises(AttributeError, match="drawn"), Plot(tmp_path / "t.svg") as plot:
        plot.drawn(10, 10)  # pyright: ignore[reportAttributeAccessIssue]
    assert not (tmp_path / "t.svg").exists()


def test_but_the_colleagues_plotter_swallows_it(tmp_path):
    with colleagues_plot()(tmp_path / "t.svg") as plot:
        plot.drawn(10, 10)  # pyright: ignore[reportAttributeAccessIssue]
    assert (tmp_path / "t.svg").exists()
