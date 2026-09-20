"""Project 14's spinning cube, in a browser, by way of pygbag.

There are three changes from the original: the loop is inside an `async def`,
it has an `await asyncio.sleep(0)` in it, and `asyncio.run` starts it.
"""

import asyncio
import math
from itertools import combinations, product

import pygame

CORNERS = list(product((-1, 1), repeat=3))
EDGES = [
    (a, b)
    for a, b in combinations(range(8), 2)
    if sum(p != q for p, q in zip(CORNERS[a], CORNERS[b], strict=True)) == 1
]


async def main() -> None:
    pygame.init()
    window = pygame.display.set_mode((480, 480))
    clock = pygame.time.Clock()
    angle = 0.0
    while all(event.type != pygame.QUIT for event in pygame.event.get()):
        angle += clock.tick(60) / 1000
        c, s = math.cos(angle), math.sin(angle)
        dots = []
        for x, y, z in CORNERS:
            x, z = x * c + z * s, z * c - x * s  # turn about the y axis
            y, z = y * c - z * s, z * c + y * s  # and then about the x axis
            dots.append((240 + 600 * x / (5 - z), 240 - 600 * y / (5 - z)))
        window.fill("black")
        for a, b in EDGES:
            pygame.draw.aaline(window, "green", dots[a], dots[b])
        pygame.display.flip()
        await asyncio.sleep(0)  # let the browser have a turn
    pygame.quit()


asyncio.run(main())
