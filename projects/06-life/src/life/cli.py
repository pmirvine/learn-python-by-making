"""The command line: choosing a pattern, and animating it in the terminal."""

import argparse
import shutil
import time
from itertools import islice

from life.core import generations
from life.patterns import PATTERNS, parse, shift, soup
from life.render import render

HOME = "\033[H"
CLEAR = "\033[2J"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"


def parse_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="life", description="Conway's Game of Life, in the terminal."
    )
    parser.add_argument(
        "pattern",
        nargs="?",
        default="soup",
        choices=["soup", *PATTERNS],
        help="what to start with (default: random soup)",
    )
    parser.add_argument("-g", "--generations", type=int, help="stop after this many")
    parser.add_argument("--fps", type=float, default=10, help="generations a second")
    parser.add_argument("--seed", type=int, help="make the soup repeatable")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_arguments(argv)
    columns, lines = shutil.get_terminal_size()
    width, height = columns // 2, lines - 2

    if args.pattern == "soup":
        live = soup(width, height, seed=args.seed)
    else:
        live = shift(parse(PATTERNS[args.pattern]), width // 3, height // 3)

    print(CLEAR + HIDE_CURSOR, end="")
    try:
        history = islice(generations(live), args.generations)
        for number, universe in enumerate(history):
            print(HOME + render(universe, width, height))
            status = f"Generation {number}, population {len(universe)}  "
            print(status, end="", flush=True)
            time.sleep(1 / args.fps)
    except KeyboardInterrupt:
        pass
    finally:
        print(SHOW_CURSOR)
