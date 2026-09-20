"""Bouncing lines, with the vanishing trail fixed."""

import random

import beeb

TRAIL = 24
LIMITS = [beeb.WIDTH - 1, beeb.HEIGHT - 1, beeb.WIDTH - 1, beeb.HEIGHT - 1]

type Line = list[float]


def bounce(position: float, velocity: float, limit: int) -> tuple[float, float]:
    """Move one coordinate along, turning round if it would leave 0 to limit."""
    if not 0 <= position + velocity <= limit:
        velocity = -velocity
    return position + velocity, velocity


def step(line: Line, velocity: Line) -> None:
    """Move the line on by one frame. Updates both lists in place: no garbage!"""
    for i, limit in enumerate(LIMITS):
        line[i], velocity[i] = bounce(line[i], velocity[i], limit)


def remember(trail: list[tuple[Line, int]], line: Line, colour: int) -> None:
    """Add the line to the trail, and forget the oldest if the trail is full."""
    trail.append((line.copy(), colour))
    del trail[:-TRAIL]


def main() -> None:
    beeb.mode(2)
    line = [float(random.randint(0, limit)) for limit in LIMITS]
    velocity = [random.choice([-1, 1]) * random.uniform(6, 20) for _ in LIMITS]
    trail: list[tuple[Line, int]] = []
    frame = 0

    while True:
        step(line, velocity)
        remember(trail, line, frame // 8 % 7 + 1)

        beeb.clg()
        for (x1, y1, x2, y2), colour in trail:
            beeb.gcol(0, colour)
            beeb.move(x1, y1)
            beeb.draw(x2, y2)
        beeb.vsync()
        frame += 1


if __name__ == "__main__":
    main()
