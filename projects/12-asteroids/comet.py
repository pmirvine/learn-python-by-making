from collections import deque

import pygame


class Trail:
    def __init__(self, length):
        self.points = deque(maxlen=length)

    def __iadd__(self, point):
        self.points.append(point)
        return self

    def __len__(self):
        return len(self.points)

    def __getitem__(self, index):
        return self.points[index]


pygame.init()
window = pygame.display.set_mode((640, 512))
clock = pygame.time.Clock()
trail = Trail(40)

while not pygame.event.get(pygame.QUIT):
    trail += pygame.mouse.get_pos()
    window.fill("black")
    for age, point in enumerate(trail):
        shade = 255 * age // len(trail)
        pygame.draw.circle(window, (shade, shade, 0), point, 1 + age // 3)
    pygame.draw.circle(window, "white", trail[-1], 6)
    pygame.display.flip()
    clock.tick(60)
