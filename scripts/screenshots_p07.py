"""Regenerate the Project 7 pictures.

    uv run --project projects/07-fractal-factory python scripts/screenshots_p07.py

The pictures are made by the project's own command line, so they can't drift.
"""

import importlib.util
from pathlib import Path

from fractals import PALETTES, black_inside, julia, render
from fractals.cli import main as fractal

ROOT = Path(__file__).parent.parent
ASSETS = ROOT / "docs" / "assets"
P07 = ROOT / "projects" / "07-fractal-factory"

PICTURES = {
    "p07-mandelbrot.png": ["mandelbrot", "--palette", "ocean", "--cycles", "3"],
    "p07-julia.png": ["julia", "--palette", "fire", "--cycles", "2"],
    "p07-plasma.png": ["plasma", "--palette", "beeb", "--cycles", "2"],
    "p07-seahorses.png": [
        "mandelbrot",
        "--centre=-0.745+0.113j",
        "--width",
        "0.02",
        "--limit",
        "300",
        "--palette",
        "beeb",
        "--cycles",
        "6",
    ],
}


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    for picture, arguments in PICTURES.items():
        fractal([*arguments, "-o", str(ASSETS / picture)])

    # Stage 1's picture is in greys, from the stage's own code.
    fields = load(P07 / "stages" / "stage1_fields.py", "stage1_fields")
    stage1 = load(P07 / "stages" / "stage1_render.py", "stage1_render")
    stage1.render(fields.mandelbrot, centre=-0.6 + 0j, width=3.6).save(
        ASSETS / "p07-grey.png"
    )

    # The late-binding gotcha: three Julia sets that all come out the same.
    constants = [-0.8 + 0.156j, 0.285 + 0.01j, -0.4 + 0.6j]
    wrong = [lambda point: julia(c)(point) for c in constants]  # noqa: B023 - the bug on show
    right = [julia(c) for c in constants]
    palette = black_inside(PALETTES["fire"])
    for label, fields_ in (("wrong", wrong), ("right", right)):
        strip = None
        for index, field in enumerate(fields_):
            tile = render(field, palette, size=(210, 160), width=3.4)
            if strip is None:
                strip = tile.resize((640, 160))
                strip.paste((0, 0, 0), (0, 0, 640, 160))
            strip.paste(tile, (5 + index * 215, 0))
        strip.save(ASSETS / f"p07-julias-{label}.png")
        print(f"Saved p07-julias-{label}.png")


if __name__ == "__main__":
    main()
