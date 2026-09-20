import random

import pygame

SIZE = 512


class Star:
    def __init__(self):
        self.x, self.y = random.uniform(-1, 1), random.uniform(-1, 1)
        self.z = random.uniform(0.05, 1)

    @property
    def screen(self):
        return SIZE / 2 * (1 + self.x / self.z), SIZE / 2 * (1 + self.y / self.z)

    @property
    def shade(self):
        return int(255 * (1 - self.z))

    def approach(self, seconds):
        self.z -= 0.3 * seconds
        if self.z < 0.01:
            self.z = 1.0


pygame.init()
window = pygame.display.set_mode((SIZE, SIZE))
clock = pygame.time.Clock()
stars = [Star() for _ in range(300)]

while not pygame.event.get(pygame.QUIT):
    seconds = clock.tick(60) / 1000
    window.fill("black")
    for star in stars:
        star.approach(seconds)
        pygame.draw.circle(window, [star.shade] * 3, star.screen, 1 + star.shade // 128)
    pygame.display.flip()
