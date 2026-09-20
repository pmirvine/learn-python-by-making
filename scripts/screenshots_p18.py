"""Regenerate the Project 18 pictures, which are SVG files, drawn by the examples.

uv run --project projects/18-svg-plotter python scripts/screenshots_p18.py
"""

import runpy
import shutil
import tempfile
from contextlib import chdir
from pathlib import Path

ROOT = Path(__file__).parent.parent
P18 = ROOT / "projects" / "18-svg-plotter"
ASSETS = ROOT / "docs" / "assets"


def main() -> None:
    with tempfile.TemporaryDirectory() as scratch, chdir(scratch):
        for example in ("rose", "maze", "hilbert"):
            runpy.run_path(str(P18 / "examples" / f"{example}.py"), run_name="__main__")
            shutil.copy(
                Path("pictures") / f"{example}.svg", ASSETS / f"p18-{example}.svg"
            )
        runpy.run_path(str(P18 / "solutions" / "chart.py"), run_name="__main__")
        shutil.copy(Path("pictures") / "chart.svg", ASSETS / "p18-chart.svg")
    print("Saved p18-rose.svg, p18-maze.svg, p18-hilbert.svg and p18-chart.svg")


if __name__ == "__main__":
    main()
