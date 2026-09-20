"""A colleague's unpack, for showing a graphics character in the terminal.

    uv run bughunt/dotty.py

It packs a small picture into graphics characters, and unpacks them again. What
comes out ought to be what went in.
"""

from pyfax.mosaic import pack

PICTURE = [
    "..####..",
    ".######.",
    "##.##.##",
    "########",
    ".#.##.#.",
    "#......#",
]


def unpack(dots: int) -> list[str]:
    """Turn one graphics character back into three rows of two pixels."""
    rows: list[str] = []
    for y in range(3):
        row = ""
        for x in range(2):
            position = y * 2 + x
            row += "#" if dots & (1 << position) == 1 else "."
        rows.append(row)
    return rows


def main() -> None:
    print("In:")
    print("\n".join(PICTURE))
    print("\nOut:")
    for line in pack(PICTURE):
        characters = [unpack(dots) for dots in line]
        for y in range(3):
            print("".join(character[y] for character in characters))


if __name__ == "__main__":
    main()
