"""Things on the screen that can be clicked, and the picture itself."""

from collections.abc import Callable

import pygame

from sprite_editor.sprite import Cell, Colour, Sprite

PALETTE = [
    (0, 0, 0), (255, 0, 0), (0, 255, 0), (255, 255, 0),
    (0, 0, 255), (255, 0, 255), (0, 255, 255), (255, 255, 255),
]  # fmt: skip
PANEL = (52, 56, 64)
RAISED = (84, 90, 102)
LIT = (255, 200, 60)
TEXT = (235, 235, 235)
CHECKS = ((150, 150, 150), (110, 110, 110))


def draw_checks(window: pygame.Surface, rect: pygame.Rect, size: int) -> None:
    """Fill a rectangle with grey squares, which is how see-through is shown."""
    for y in range(rect.top, rect.bottom, size):
        for x in range(rect.left, rect.right, size):
            shade = CHECKS[(x - rect.left + y - rect.top) // size % 2]
            square = pygame.Rect(x, y, size, size).clip(rect)
            window.fill(shade, square)


class Button:
    def __init__(
        self,
        rect: pygame.Rect,
        label: str,
        on_click: Callable[[], None],
        is_on: Callable[[], bool] = lambda: False,
    ) -> None:
        self.rect = rect
        self.label = label
        self.on_click = on_click
        self.is_on = is_on

    def draw(self, window: pygame.Surface, font: pygame.font.Font) -> None:
        window.fill(RAISED, self.rect)
        self.draw_face(window, font)
        if self.is_on():
            pygame.draw.rect(window, LIT, self.rect, width=3)

    def draw_face(self, window: pygame.Surface, font: pygame.font.Font) -> None:
        words = font.render(self.label, True, TEXT)
        window.blit(words, words.get_rect(center=self.rect.center))


class Swatch(Button):
    """A button with a colour on its face where a plain one has words."""

    def __init__(
        self,
        rect: pygame.Rect,
        colour: Colour,
        on_click: Callable[[], None],
        is_on: Callable[[], bool],
    ) -> None:
        super().__init__(rect, f"colour {colour}", on_click, is_on)
        self.colour = colour

    def draw_face(self, window: pygame.Surface, font: pygame.font.Font) -> None:
        face = self.rect.inflate(-8, -8)
        if self.colour is None:
            draw_checks(window, face, 8)
        else:
            window.fill(PALETTE[self.colour], face)


class Canvas:
    """The picture, blown up, with whatever the tool is about to do laid over it."""

    def __init__(self, rect: pygame.Rect, sprite: Sprite) -> None:
        self.zoom = min(rect.width // sprite.width, rect.height // sprite.height)
        self.rect = pygame.Rect(
            rect.left, rect.top, sprite.width * self.zoom, sprite.height * self.zoom
        )

    def cell_at(self, position: tuple[int, int]) -> Cell:
        x, y = position
        return (x - self.rect.left) // self.zoom, (y - self.rect.top) // self.zoom

    def draw(
        self, window: pygame.Surface, sprite: Sprite, changes: dict[Cell, Colour]
    ) -> None:
        draw_checks(window, self.rect, self.zoom // 2)
        showing = sprite.pixels | changes
        for (x, y), colour in showing.items():
            if colour is not None and (x, y) in sprite:
                left = self.rect.left + x * self.zoom
                top = self.rect.top + y * self.zoom
                window.fill(PALETTE[colour], (left, top, self.zoom, self.zoom))


def draw_actual_size(
    window: pygame.Surface, sprite: Sprite, corner: tuple[int, int], scale: int
) -> pygame.Rect:
    """Draw the sprite small, as it'll look in a game, and return where it went."""
    left, top = corner
    rect = pygame.Rect(left, top, sprite.width * scale, sprite.height * scale)
    window.fill((0, 0, 0), rect)
    for (x, y), colour in sprite.pixels.items():
        window.fill(PALETTE[colour], (left + x * scale, top + y * scale, scale, scale))
    return rect
