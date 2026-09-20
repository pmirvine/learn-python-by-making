"""A BBC Micro-style graphics screen, built on Pygame.

The screen is always 1280 units wide and 1024 high, with (0, 0) at the bottom
left, whichever mode you choose. Modes differ in how many real pixels, and how
many colours, you get.
"""

import pygame

WIDTH = 1280
HEIGHT = 1024
FRAME_RATE = 50
WINDOW_SIZE = (640, 512)

# Each mode's width and height in real pixels, and its number of colours.
MODES = {
    0: (640, 256, 2),
    1: (320, 256, 4),
    2: (160, 256, 16),
    4: (320, 256, 2),
    5: (160, 256, 4),
}

# The eight colours the hardware could make: every mix of red, green and blue.
COLOURS = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (255, 255, 0),
    (0, 0, 255),
    (255, 0, 255),
    (0, 255, 255),
    (255, 255, 255),
]

# Which of those eight each colour number starts out as, by colours in the mode.
DEFAULT_PALETTES = {
    2: [0, 7],
    4: [0, 1, 3, 7],
    16: [0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 4, 5, 6, 7],
}

_window: pygame.Surface | None = None
_canvas: pygame.Surface | None = None
_clock: pygame.time.Clock | None = None
_colours = 16
_ink = 7
_paper = 0
_cursor = (0, 0)


def to_pixel(x: float, y: float, width: int, height: int) -> tuple[int, int]:
    """Convert screen units to a pixel position on a width x height surface."""
    return int(x * width // WIDTH), int(height - 1 - y * height // HEIGHT)


def _need_canvas() -> pygame.Surface:
    if _canvas is None:
        raise RuntimeError("No screen yet: call beeb.mode() first")
    return _canvas


def mode(number: int) -> None:
    """Open the screen in the given mode, or change mode. Clears the screen."""
    global _window, _canvas, _clock, _colours, _ink, _paper, _cursor

    if number not in MODES:
        raise ValueError("Bad MODE")
    width, height, _colours = MODES[number]

    pygame.init()
    _window = pygame.display.set_mode(WINDOW_SIZE, pygame.SCALED | pygame.RESIZABLE)
    pygame.display.set_caption(f"MODE {number}")
    _clock = pygame.time.Clock()

    _canvas = pygame.Surface((width, height), depth=8)
    _canvas.set_palette([COLOURS[c] for c in DEFAULT_PALETTES[_colours]])

    _ink = min(_colours - 1, 7)
    _paper = 0
    _cursor = (0, 0)
    clg()


def gcol(action: int, colour: int) -> None:
    """Choose the graphics colour. Add 128 to set the background instead."""
    global _ink, _paper

    if action != 0:
        raise NotImplementedError("Only GCOL 0 (plain plotting) so far")
    if colour >= 128:
        _paper = (colour - 128) % _colours
    else:
        _ink = colour % _colours


def clg() -> None:
    """Clear the graphics screen to the background colour."""
    _need_canvas().fill(_paper)


def move(x: float, y: float) -> None:
    """Move the graphics cursor without drawing."""
    global _cursor

    _cursor = (x, y)


def draw(x: float, y: float) -> None:
    """Draw a line from the graphics cursor to x, y."""
    global _cursor

    canvas = _need_canvas()
    size = canvas.get_size()
    pygame.draw.line(canvas, _ink, to_pixel(*_cursor, *size), to_pixel(x, y, *size))
    _cursor = (x, y)


def vsync() -> None:
    """Show the screen, then wait for the next frame. Call this once per loop.

    Closing the window or pressing Escape ends the program.
    """
    canvas = _need_canvas()
    assert _window is not None and _clock is not None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            raise SystemExit

    _window.blit(pygame.transform.scale(canvas, _window.get_size()), (0, 0))
    pygame.display.flip()
    _clock.tick(FRAME_RATE)
