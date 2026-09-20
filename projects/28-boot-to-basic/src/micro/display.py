"""Putting it all on the screen: the graphics, then the sprites, then the text."""

import pygame
from pyfax import Cell, Colour

from micro.sprites import SpriteLayer
from micro.textscreen import TextScreen

CELL_WIDTH, CELL_HEIGHT = 16, 20
TOP = 6  # twenty-five rows of twenty make 500, and the window is 512 high
FONTS = "menlo,consolas,dejavusansmono,liberationmono,couriernew,courier"
# The six squares of a graphics character: two across, and three down.
SIXELS = [
    pygame.Rect(x * 8, y, 8, high)
    for y, high in [(0, 7), (7, 6), (13, 7)]
    for x in (0, 1)
]


def rgb(colour: Colour) -> tuple[int, int, int]:
    """There's a bit each for red, green and blue, as there was in Project 19."""
    return (255 * (colour & 1), 255 * (colour >> 1 & 1), 255 * (colour >> 2 & 1))


class Display:
    def __init__(self) -> None:
        pygame.font.init()
        self.font = pygame.font.Font(pygame.font.match_font(FONTS), 20)
        self.glyphs: dict[tuple[str, Colour], pygame.Surface] = {}

    def glyph(self, character: str, ink: Colour) -> pygame.Surface:
        """Return a character's picture, stretched to fill a cell. Each is made once, and kept."""
        if (character, ink) not in self.glyphs:
            drawn = self.font.render(character, True, rgb(ink))
            size = (CELL_WIDTH, CELL_HEIGHT)
            self.glyphs[character, ink] = pygame.transform.smoothscale(drawn, size)
        return self.glyphs[character, ink]

    def cell(self, window: pygame.Surface, cell: Cell, column: int, row: int) -> None:
        place = pygame.Rect(
            column * CELL_WIDTH, TOP + row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT
        )
        if cell.paper != Colour.BLACK:
            window.fill(rgb(cell.paper), place)
        if cell.dots:
            for bit, square in enumerate(SIXELS):
                if cell.dots & (1 << bit):
                    window.fill(rgb(cell.ink), square.move(place.topleft))
        elif cell.text != " ":
            glyph = self.glyph(cell.text, cell.ink)
            window.blit(glyph, place)

    def show(
        self,
        canvas: pygame.Surface,
        sprites: SpriteLayer,
        screen: TextScreen,
        cursor: bool,
    ) -> None:
        window = pygame.display.get_surface()
        assert window is not None
        picture = pygame.Surface(canvas.get_size())
        picture.blit(canvas, (0, 0))
        sprites.draw(picture)
        pygame.transform.scale(picture, window.get_size(), window)

        for row, cells in enumerate(screen.page.rows):
            for column, cell in enumerate(cells):
                if cell.text != " " or cell.dots or cell.paper != Colour.BLACK:
                    self.cell(window, cell, column, row)
        if cursor:
            left, top = screen.column * CELL_WIDTH, TOP + screen.row * CELL_HEIGHT
            window.fill(rgb(screen.ink), (left, top + CELL_HEIGHT - 3, CELL_WIDTH, 2))
        pygame.display.flip()
