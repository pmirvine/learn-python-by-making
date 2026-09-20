"""Extend 1: writing RLE, so that what you draw can be saved and shared."""

from itertools import groupby

from life import Cell


def to_rle(live: set[Cell]) -> str:
    """Return a pattern as RLE text, with its top left corner at the origin."""
    if not live:
        return "x = 0, y = 0, rule = B3/S23\n!\n"
    left, top = min(x for x, _ in live), min(y for _, y in live)
    width = max(x for x, _ in live) - left + 1
    height = max(y for _, y in live) - top + 1

    rows = []
    for y in range(top, top + height):
        tags = ["o" if (x, y) in live else "b" for x in range(left, left + width)]
        runs = [(tag, len(list(group))) for tag, group in groupby(tags)]
        if runs and runs[-1][0] == "b":
            runs.pop()  # dead cells at the end of a row go without saying
        rows.append(
            "".join(f"{count if count > 1 else ''}{tag}" for tag, count in runs)
        )

    return f"x = {width}, y = {height}, rule = B3/S23\n{'$'.join(rows)}!\n"
