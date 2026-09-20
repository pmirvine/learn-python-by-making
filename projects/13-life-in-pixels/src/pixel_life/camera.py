"""A camera: which part of an endless universe is on the screen, and how big it looks."""

import math
from dataclasses import dataclass

from life import Cell

MIN_ZOOM, MAX_ZOOM = 1.0, 64.0

type Pixel = tuple[int, int]


@dataclass
class Camera:
    """The cell at the top left of the window, and the size of a cell in pixels."""

    x: float = 0.0
    y: float = 0.0
    zoom: float = 8.0

    def cell_at(self, pixel: Pixel) -> Cell:
        """Return the cell that's under a pixel of the window."""
        px, py = pixel
        return math.floor(self.x + px / self.zoom), math.floor(self.y + py / self.zoom)

    def pixel_of(self, cell: Cell) -> Pixel:
        """Return the pixel at the top left corner of a cell. It may be off the screen."""
        cx, cy = cell
        return round((cx - self.x) * self.zoom), round((cy - self.y) * self.zoom)

    def pan(self, dx: float, dy: float) -> None:
        """Slide the view by some pixels, as if the universe had been dragged."""
        self.x -= dx / self.zoom
        self.y -= dy / self.zoom

    def zoom_about(self, pixel: Pixel, factor: float) -> None:
        """Zoom in or out, keeping whatever is under the pixel where it is."""
        px, py = pixel
        before_x, before_y = self.x + px / self.zoom, self.y + py / self.zoom
        self.zoom = max(MIN_ZOOM, min(MAX_ZOOM, self.zoom * factor))
        self.x = before_x - px / self.zoom
        self.y = before_y - py / self.zoom

    def centre_on(self, cell: Cell, size: Pixel) -> None:
        """Move the view so that a cell is in the middle of a window of this size."""
        self.x = cell[0] - size[0] / self.zoom / 2
        self.y = cell[1] - size[1] / self.zoom / 2
