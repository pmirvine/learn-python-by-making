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
_previous = (0, 0)


def to_pixel(x: float, y: float, width: int, height: int) -> tuple[int, int]:
    """Convert screen units to a pixel position on a width x height surface."""
    return int(x * width // WIDTH), int(height - 1 - y * height // HEIGHT)


def _need_canvas() -> pygame.Surface:
    if _canvas is None:
        raise RuntimeError("No screen yet: call beeb.mode() first")
    return _canvas


def mode(number: int) -> None:
    """Open the screen in the given mode, or change mode. Clears the screen."""
    global _window, _canvas, _clock, _colours, _ink, _paper, _cursor, _previous

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
    _cursor = _previous = (0, 0)
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


def plot(k: int, x: float, y: float) -> None:
    """The do-everything drawing command: PLOT k, x, y.

    k is 0-7 for lines, 64-71 for single points, 80-87 for filled triangles.
    Within each group of eight: 0-3 measure x, y from the last point and 4-7
    from the origin; then 0 just moves, 1 draws in the graphics colour and
    3 draws in the background colour.
    """
    global _cursor, _previous

    canvas = _need_canvas()
    size = canvas.get_size()
    shape, how = divmod(k, 8)
    if how < 4:
        x, y = _cursor[0] + x, _cursor[1] + y

    match how % 4:
        case 0:
            colour = None
        case 1:
            colour = _ink
        case 3:
            colour = _paper
        case _:
            raise NotImplementedError("Inverse plotting isn't supported")

    if colour is not None:
        here = to_pixel(x, y, *size)
        match shape:
            case 0:
                pygame.draw.line(canvas, colour, to_pixel(*_cursor, *size), here)
            case 8:
                canvas.set_at(here, colour)
            case 10:
                corners = [to_pixel(*_previous, *size), to_pixel(*_cursor, *size), here]
                pygame.draw.polygon(canvas, colour, corners)
            case _:
                raise ValueError(f"PLOT {k} isn't supported")

    _previous, _cursor = _cursor, (x, y)


def move(x: float, y: float) -> None:
    """Move the graphics cursor without drawing."""
    plot(4, x, y)


def draw(x: float, y: float) -> None:
    """Draw a line from the graphics cursor to x, y."""
    plot(5, x, y)


def point(x: float, y: float) -> int:
    """Return the colour number at x, y, or -1 if that's off the screen."""
    canvas = _need_canvas()
    pixel = to_pixel(x, y, *canvas.get_size())
    if not canvas.get_rect().collidepoint(pixel):
        return -1
    return canvas.get_at_mapped(pixel)


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
