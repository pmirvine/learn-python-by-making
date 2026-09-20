"""The command line: fractal mandelbrot --palette fire -o picture.png"""

import argparse
import time
from pathlib import Path

from fractals.fields import julia, mandelbrot, plasma
from fractals.palettes import PALETTES, black_inside, cycled
from fractals.render import render


def parse_size(text: str) -> tuple[int, int]:
    """Turn "640x480" into (640, 480)."""
    try:
        columns, rows = text.lower().split("x")
        return int(columns), int(rows)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"{text!r} isn't a size such as 640x480"
        ) from None


def parse_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="fractal", description="Pictures from formulas."
    )
    parser.add_argument("field", choices=["mandelbrot", "julia", "plasma"])
    parser.add_argument(
        "-o", "--output", type=Path, help="where to save (default: FIELD.png)"
    )
    parser.add_argument(
        "--size", type=parse_size, default=(640, 480), help="such as 800x600"
    )
    parser.add_argument(
        "--centre", type=complex, help="the middle of the picture, such as -0.75+0.1j"
    )
    parser.add_argument(
        "--width", type=float, help="how much of the plane to show, left to right"
    )
    parser.add_argument(
        "--limit", type=int, default=100, help="how long to wait for a point to escape"
    )
    parser.add_argument(
        "--c", type=complex, default=-0.8 + 0.156j, help="the constant of a Julia set"
    )
    parser.add_argument("--palette", choices=list(PALETTES), default="fire")
    parser.add_argument(
        "--cycles", type=int, default=1, help="run through the palette this many times"
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_arguments(argv)

    if args.field == "mandelbrot":
        field, centre, width = mandelbrot(args.limit), -0.6 + 0j, 3.6
    elif args.field == "julia":
        field, centre, width = julia(args.c, args.limit), 0j, 3.6
    else:
        field, centre, width = plasma(), 0j, 6.0

    palette = cycled(PALETTES[args.palette], args.cycles)
    if args.field != "plasma":
        palette = black_inside(palette)

    started = time.perf_counter()
    image = render(
        field,
        palette,
        size=args.size,
        centre=centre if args.centre is None else args.centre,
        width=width if args.width is None else args.width,
    )
    output = args.output or Path(f"{args.field}.png")
    image.save(output)
    print(f"Saved {output} in {time.perf_counter() - started:.1f} seconds.")
