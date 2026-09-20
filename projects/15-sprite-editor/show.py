import sys
from pathlib import Path

RESET = "\x1b[0m"


def paint(top: str, bottom: str) -> str:
    """Return one character that shows two pixels, one above the other."""
    if top == bottom == ".":
        return RESET + " "
    if top == ".":
        return f"{RESET}\x1b[3{bottom}m▄"
    if bottom == ".":
        return f"{RESET}\x1b[3{top}m▀"
    return f"\x1b[3{top};4{bottom}m▀"


lines = Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()
rows = [line for line in lines if line and line[0] in ".01234567"]
if len(rows) % 2:
    rows.append("." * len(rows[0]))

for upper, lower in zip(rows[::2], rows[1::2], strict=True):
    print("".join(paint(*pair) for pair in zip(upper, lower, strict=True)) + RESET)
