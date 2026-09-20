"""Bouncing lines with a longer trail, reflected left to right: a kaleidoscope."""

import random

import beeb

TRAIL = 40
LIMITS = [beeb.WIDTH - 1, beeb.HEIGHT - 1, beeb.WIDTH - 1, beeb.HEIGHT - 1]

type Line = list[float]


def bounce(position: float, velocity: float, limit: int) -> tuple[float, float]:
    """Move one coordinate along, turning round if it would leave 0 to limit."""
    if not 0 <= position + velocity <= limit:
        velocity = -velocity
    return position + velocity, velocity


def step(line: Line, velocity: Line) -> tuple[Line, Line]:
    """Return where the line is a frame later, and its new velocity."""
    moved = [bounce(*pvl) for pvl in zip(line, velocity, LIMITS, strict=True)]
    return [p for p, _ in moved], [v for _, v in moved]


def main() -> None:
    beeb.mode(2)
    line = [float(random.randint(0, limit)) for limit in LIMITS]
    velocity = [random.choice([-1, 1]) * random.uniform(6, 20) for _ in LIMITS]
    trail: list[tuple[Line, int]] = []
    frame = 0

    while True:
        line, velocity = step(line, velocity)
        trail.append((line, frame // 8 % 7 + 1))
        del trail[:-TRAIL]

        beeb.clg()
        for (x1, y1, x2, y2), colour in trail:
            beeb.gcol(0, colour)
            beeb.move(x1, y1)
            beeb.draw(x2, y2)
            beeb.move(beeb.WIDTH - 1 - x1, y1)
            beeb.draw(beeb.WIDTH - 1 - x2, y2)
        beeb.vsync()
        frame += 1


if __name__ == "__main__":
    main()
