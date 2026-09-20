"""Drawing a ship."""

from enum import Enum, auto

import pygame

from wireframe.matrix import Matrix
from wireframe.model import Ship
from wireframe.projection import brightness, faces_the_eye, project

BLACK = (0, 0, 0)
LINES = (255, 255, 255)
TEXT = (255, 255, 0)
DIMMEST = 0.2  # how bright a face is when it gets no light at all


class Style(Enum):
    WIRES = auto()
    HIDDEN = auto()
    SOLID = auto()


class View:
    def __init__(self, window: pygame.Surface) -> None:
        self.window = window
        self.font = pygame.font.Font(None, 20)

    def draw(
        self,
        ship: Ship,
        orientation: Matrix,
        distance: float,
        style: Style,
        message: str = "",
    ) -> None:
        self.window.fill(BLACK)
        width, height = self.window.get_size()
        centre = (width // 2, height // 2)

        turned = [orientation @ point for point in ship.points]
        for face in ship.faces:
            corners = [turned[number] for number in face.points]
            if style is not Style.WIRES and not faces_the_eye(corners, distance):
                continue
            outline = [project(corner, distance, height, centre) for corner in corners]
            if style is Style.SOLID:
                light = DIMMEST + (1 - DIMMEST) * brightness(corners)
                colour = pygame.Color(face.colour).lerp(BLACK, 1 - light)
                pygame.draw.polygon(self.window, colour, outline)
            else:
                pygame.draw.polygon(self.window, LINES, outline, width=1)

        self.write(message or ship.name.upper(), height - 22)

    def write(self, text: str, y: int) -> None:
        picture = self.font.render(text, False, TEXT)
        x = (self.window.get_width() - picture.get_width()) // 2
        self.window.blit(picture, (x, y))
