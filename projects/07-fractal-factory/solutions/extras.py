"""The challenges: a palette of your own, multibrots, and a big algorithmic win."""

import time

from fractals import (
    PALETTES,
    Field,
    black_inside,
    cycled,
    escape_time,
    gradient,
    mandelbrot,
    render,
)

# Tweak 2: a palette of your own is one line.
SUNSET = gradient((20, 0, 40), (120, 20, 80), (250, 100, 40), (255, 220, 120))


def multibrot(power: int, limit: int = 100) -> Field:
    """Extend 1: z = z ** power + c. Each call makes a field with a power of its own."""

    def field(point: complex) -> float:
        z = 0j
        for count in range(limit):
            if abs(z) > 2.0:
                return count / limit
            z = z**power + point
        return 1.0

    return field


def in_the_main_bulbs(point: complex) -> bool:
    """Is the point in the big heart-shaped region, or the circle to its left?

    Both have exact formulas, and between them they hold most of the points
    that would otherwise cost `limit` trips round the loop.
    """
    x, y = point.real, point.imag
    q = (x - 0.25) ** 2 + y * y
    in_the_heart = q * (q + (x - 0.25)) <= 0.25 * y * y
    in_the_circle = (x + 1) ** 2 + y * y <= 0.0625
    return in_the_heart or in_the_circle


def quick_mandelbrot(limit: int = 100) -> Field:
    """Extend 2: the Mandelbrot set, without working out what's already known."""

    def field(point: complex) -> float:
        if in_the_main_bulbs(point):
            return 1.0
        return escape_time(0j, point, limit)

    return field


def main() -> None:
    palette = black_inside(cycled(PALETTES["ocean"], 3))
    for name, field in [
        ("mandelbrot", mandelbrot(500)),
        ("quick_mandelbrot", quick_mandelbrot(500)),
    ]:
        started = time.perf_counter()
        render(field, palette, centre=-0.6 + 0j, width=3.6)
        print(f"{name:18} {time.perf_counter() - started:.2f} seconds")

    for power in (3, 4, 5):
        render(multibrot(power), black_inside(SUNSET), width=3.0).save(
            f"multibrot{power}.png"
        )
    print("Saved multibrot3.png, multibrot4.png and multibrot5.png.")


if __name__ == "__main__":
    main()
