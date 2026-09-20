"""A BBC Micro-style graphics screen, built on Pygame.

The screen is always 1280 units wide and 1024 high, with (0, 0) at the bottom
left, whichever mode you choose. Modes differ in how many real pixels, and how
many colours, you get.

This is the challenge-solutions version. On top of the chapter's module it adds
colour() to redefine the palette, flashing colours 8 to 15, fill() and circle().
"""

import pygame

WIDTH = 1280
HEIGHT = 1024
FRAME_RATE = 50
FLASH_FRAMES = 25
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
# "Physical" colours 8 to 15 flash between one of these and its opposite.
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
    16: list(range(16)),
}

_window: pygame.Surface | None = None
_canvas: pygame.Surface | None = None
_clock: pygame.time.Clock | None = None
_colours = 16
_ink = 7
_paper = 0
_cursor = (0, 0)
_previous = (0, 0)
_keys: list[str] = []
_palette: list[int] = []
_frame = 0


def to_pixel(x: float, y: float, width: int, height: int) -> tuple[int, int]:
    """Convert screen units to a pixel position on a width x height surface."""
    return int(x * width // WIDTH), int(height - 1 - y * height // HEIGHT)


def to_units(px: int, py: int, width: int, height: int) -> tuple[int, int]:
    """Convert a pixel position on a width x height surface to screen units."""
    return px * WIDTH // width, (height - 1 - py) * HEIGHT // height


def _need_canvas() -> pygame.Surface:
    if _canvas is None:
        raise RuntimeError("No screen yet: call beeb.mode() first")
    return _canvas


def _apply_palette() -> None:
    """Load the palette into the canvas, resolving flashing colours for this moment."""
    canvas = _need_canvas()
    first_half = _frame // FLASH_FRAMES % 2 == 0
    for logical, physical in enumerate(_palette):
        if physical >= 8:
            physical = physical - 8 if first_half else 15 - physical
        canvas.set_palette_at(logical, COLOURS[physical])


def mode(number: int) -> None:
    """Open the screen in the given mode, or change mode. Clears the screen."""
    global _window, _canvas, _clock, _colours, _ink, _paper, _cursor, _previous
    global _palette, _frame

    if number not in MODES:
        raise ValueError("Bad MODE")
    width, height, _colours = MODES[number]

    pygame.init()
    _window = pygame.display.set_mode(WINDOW_SIZE, pygame.SCALED | pygame.RESIZABLE)
    pygame.display.set_caption(f"MODE {number}")
    _clock = pygame.time.Clock()

    _canvas = pygame.Surface((width, height), depth=8)
    _palette = DEFAULT_PALETTES[_colours].copy()
    _frame = 0
    _apply_palette()

    _ink = min(_colours - 1, 7)
    _paper = 0
    _cursor = _previous = (0, 0)
    _keys.clear()
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


def colour(logical: int, physical: int) -> None:
    """Change what a colour number looks like on screen: the BBC's VDU 19.

    Everything already drawn in that colour number changes too, instantly.
    """
    _palette[logical % _colours] = physical % 16
    _apply_palette()


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


def fill(x: float, y: float) -> None:
    """Flood-fill outwards from x, y in the graphics colour."""
    canvas = _need_canvas()
    pixel = to_pixel(x, y, *canvas.get_size())
    if canvas.get_rect().collidepoint(pixel):
        pygame.draw.flood_fill(canvas, _ink, pixel)


def circle(x: float, y: float, radius: float) -> None:
    """Draw a circle outline. Pixels aren't square, so in pixels it's an ellipse."""
    canvas = _need_canvas()
    width, height = canvas.get_size()
    left, top = to_pixel(x - radius, y + radius, width, height)
    right, bottom = to_pixel(x + radius, y - radius, width, height)
    box = pygame.Rect(left, top, right - left + 1, bottom - top + 1)
    pygame.draw.ellipse(canvas, _ink, box, width=1)


def vsync() -> None:
    """Show the screen, then wait for the next frame. Call this once per loop.

    Closing the window or pressing Escape ends the program.
    """
    global _frame

    canvas = _need_canvas()
    assert _window is not None and _clock is not None

    _frame += 1
    if _frame % FLASH_FRAMES == 0:
        _apply_palette()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            if event.unicode:
                _keys.append(event.unicode)

    _window.blit(pygame.transform.scale(canvas, _window.get_size()), (0, 0))
    pygame.display.flip()
    _clock.tick(FRAME_RATE)


def inkey() -> str:
    """Return the next key typed, or an empty string if there isn't one."""
    return _keys.pop(0) if _keys else ""


def mouse() -> tuple[int, int, tuple[bool, bool, bool]]:
    """Return the mouse position in screen units, and its (left, middle, right) buttons."""
    if _window is None:
        raise RuntimeError("No screen yet: call beeb.mode() first")
    x, y = to_units(*pygame.mouse.get_pos(), *_window.get_size())
    return x, y, pygame.mouse.get_pressed()


def screenshot(path: str) -> None:
    """Save the screen as an image file, such as a .png."""
    canvas = _need_canvas()
    pygame.image.save(pygame.transform.scale(canvas, WINDOW_SIZE), path)
