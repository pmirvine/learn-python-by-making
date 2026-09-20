"""Fractal Factory: pictures from formulas."""

from fractals.fields import mandelbrot, plasma
from fractals.render import render


def main() -> None:
    render(mandelbrot, centre=-0.6 + 0j, width=3.6).save("mandelbrot.png")
    render(plasma, width=6.0).save("plasma.png")
    print("Saved mandelbrot.png and plasma.png.")
