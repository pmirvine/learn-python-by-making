"""A stand-in for Pyxel, which needs OpenGL and so can't run where there's no display.

It has the handful of functions that the side quest uses, keeps a record of what
was drawn in each frame, and "runs" a game for a fixed number of frames, with
whichever keys the test says are held down. A test checks that everything here
has a real counterpart of the same name, so that it can't drift into fiction.
"""

import random
from collections.abc import Callable

KEY_LEFT, KEY_RIGHT, KEY_SPACE = 1, 2, 3

width = height = frame_count = 0
calls: list[tuple] = []  # what the current frame drew
frames: list[list[tuple]] = []  # and all the frames before it
played: list[tuple[int, int]] = []
held: Callable[[int], set[int]] = lambda frame: set()
frames_to_run = 0
_rng = random.Random(15)


class Image:
    def __init__(self) -> None:
        self.rows: list[str] = []

    def set(self, x: int, y: int, rows: list[str]) -> None:
        assert (x, y) == (0, 0)
        assert all(set(row) <= set("0123456789abcdef") for row in rows), rows
        self.rows = rows


class Sound:
    def __init__(self) -> None:
        self.settings: tuple = ()

    def set(
        self, notes: str, tones: str, volumes: str, effects: str, speed: int
    ) -> None:
        self.settings = (notes, tones, volumes, effects, speed)


images = [Image() for _ in range(3)]
sounds = [Sound() for _ in range(64)]


def reset(frames_wanted: int, keys: Callable[[int], set[int]]) -> None:
    global frame_count, frames_to_run, held
    frame_count, frames_to_run, held = 0, frames_wanted, keys
    calls.clear()
    frames.clear()
    played.clear()
    _rng.seed(15)


def init(w: int, h: int, title: str = "", fps: int = 30) -> None:
    global width, height
    width, height = w, h
    calls.append(("init", w, h, title, fps))


def run(update: Callable[[], None], draw: Callable[[], None]) -> None:
    global frame_count
    for _ in range(frames_to_run):
        calls.clear()
        update()
        draw()
        frames.append(list(calls))
        frame_count += 1


def btn(key: int) -> bool:
    return key in held(frame_count)


def btnp(key: int) -> bool:
    return key in held(frame_count) and key not in held(frame_count - 1)


def rndi(low: int, high: int) -> int:
    return _rng.randint(low, high)


def rndf(low: float, high: float) -> float:
    return _rng.uniform(low, high)


def play(channel: int, sound: int) -> None:
    played.append((channel, sound))


def cls(colour: int) -> None:
    calls.append(("cls", colour))


def pset(x: float, y: float, colour: int) -> None:
    calls.append(("pset", x, y, colour))


def circ(x: float, y: float, radius: float, colour: int) -> None:
    calls.append(("circ", x, y, radius, colour))


def text(x: float, y: float, words: str, colour: int) -> None:
    calls.append(("text", x, y, words, colour))


def blt(
    x: float, y: float, image: int, u: int, v: int, w: int, h: int, key: int
) -> None:
    calls.append(("blt", x, y, image, u, v, w, h, key))
