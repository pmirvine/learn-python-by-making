import math
import xml.etree.ElementTree as ET

from chart import chart

from plotter import Plot

SVG = "{http://www.w3.org/2000/svg}"


def test_a_chart_has_axes_ticks_a_curve_and_a_name(tmp_path):
    plot = Plot(tmp_path / "chart.svg")
    chart(plot, math.sin, (0, 6), (-1, 1), "y = sin x, where 0 < x & x < 6")
    tree = ET.fromstring(plot.svg())
    paths = list(tree.iter(f"{SVG}path"))
    assert len(paths) == 2 + 7 + 1
    assert paths[-1].get("stroke") == "yellow"
    assert paths[-1].get("d", "").count("L") == 400
    labels = [text.text for text in tree.iter(f"{SVG}text")]
    assert labels[:-1] == ["0", "1", "2", "3", "4", "5", "6"]
    assert labels[-1] == "y = sin x, where 0 < x & x < 6"
