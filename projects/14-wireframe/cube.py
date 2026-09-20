import math
from itertools import combinations, product

import pygame

CORNERS = list(product((-1, 1), repeat=3))
EDGES = [
    (a, b)
    for a, b in combinations(range(8), 2)
    if sum(p != q for p, q in zip(CORNERS[a], CORNERS[b], strict=True)) == 1
]

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
pygame.quit()
