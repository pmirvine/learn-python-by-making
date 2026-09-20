"""An authoring aid: fill a chapter's listings in from the real files.

    uv run scripts/fill_listings.py docs/part-2-pygame/p10-breakout.md

While drafting a chapter, put a directive where the code should go, inside a
fenced block that has a listing marker above it:

    <!-- listing: projects/10-breakout/src/breakout/model.py -->
    ```python title="src/breakout/model.py"
    #@ from: class Level: | to: class Bat:
    ```

and this script replaces the directive with those lines of the file: from the
first line containing the `from` text, up to but not including the first line
after it containing the `to` text. `from: START` and `to: END` mean the ends of
the file. Several directives in one block are joined with `# ...` lines.

The filled-in chapter is what gets committed, and scripts/check_docs.py goes on
verifying it, so a listing can't drift even if this script is never run again.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
MARKER = re.compile(r"^\s*<!--\s*listing:\s*(?P<path>\S+)\s*-->\s*$")
DIRECTIVE = re.compile(
    r"^(?P<indent>\s*)#@ from: (?P<start>.+?) \| to: (?P<end>.+?)\s*$"
)


def segment(source: list[str], start: str, end: str, where: str) -> list[str]:
    first = 0
    if start != "START":
        matches = [n for n, line in enumerate(source) if start in line]
        if not matches:
            raise SystemExit(f"{where}: nothing in the file contains {start!r}")
        first = matches[0]
    last = len(source)
    if end != "END":
        matches = [n for n in range(first + 1, len(source)) if end in source[n]]
        if not matches:
            raise SystemExit(f"{where}: nothing after that contains {end!r}")
        last = matches[0]
    lines = source[first:last]
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def fill(chapter: Path) -> int:
    lines = chapter.read_text(encoding="utf-8").split("\n")
    source: list[str] = []
    filled = 0
    result = []
    for number, line in enumerate(lines, start=1):
        if found := MARKER.match(line):
            path = ROOT / found["path"]
            source = (
                path.read_text(encoding="utf-8").split("\n") if path.is_file() else []
            )
        if found := DIRECTIVE.match(line):
            where = f"{chapter.name}:{number}"
            if not source:
                raise SystemExit(
                    f"{where}: a directive with no listing marker above it"
                )
            if result and DIRECTIVE.match(lines[number - 2]):
                result.append(found["indent"] + "# ...")
            for code in segment(source, found["start"], found["end"], where):
                result.append(found["indent"] + code if code.strip() else "")
            filled += 1
        else:
            result.append(line)
    chapter.write_text("\n".join(result), encoding="utf-8")
    return filled


def main() -> None:
    for name in sys.argv[1:]:
        print(f"{name}: filled {fill(Path(name))} listings")


if __name__ == "__main__":
    main()
