"""Check that the code shown in the chapters is true.

    uv run scripts/check_docs.py

Three checks, described for authors in STYLE.md:

1. A fenced block preceded by `<!-- listing: path -->` must appear, verbatim,
   in that file. A line containing only `# ...` splits the block into pieces,
   which must all appear, in order. Python blocks with a `title=` must have a
   marker (`<!-- listing: none -->` to opt out).
2. `pycon` blocks are run as doctests, top to bottom through each chapter,
   sharing state. `<!-- no-doctest -->` opts a block out.
3. The snippet in a "Predict" box is run, and what it prints is compared with
   the first `text` block in the "Answer" box after it. `<!-- no-check -->`
   before the snippet opts out.
"""

import contextlib
import doctest
import io
import logging
import os
import re
import sys
import textwrap
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# Pygame announces itself when it's first imported, which would look like
# unexpected output to a doctest. It also mustn't try to open a window.
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

FENCE = re.compile(r"^(?P<indent>\s*)(?P<ticks>`{3,})(?P<lang>[\w-]*)(?P<attrs>.*)$")
MARKER = re.compile(
    r"^\s*<!--\s*(?P<kind>listing|no-doctest|no-check)\s*:?\s*(?P<arg>.*?)\s*-->\s*$"
)
ADMONITION = re.compile(r'^(?P<indent>\s*)(?:!!!|\?\?\?\+?)\s+\w+\s+"(?P<title>[^"]*)"')
ELISION = "# ..."


@dataclass
class Block:
    path: Path
    line: int
    lang: str
    attrs: str
    code: str
    marker: tuple[str, str] | None
    box: str

    @property
    def where(self) -> str:
        return f"{self.path.relative_to(ROOT)}:{self.line}"


def blocks_in(path: Path) -> list[Block]:
    """Find every fenced code block, with the marker before it and the box around it."""
    blocks: list[Block] = []
    marker: tuple[str, str] | None = None
    box, box_indent = "", -1
    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        indent = len(line) - len(line.lstrip())

        if line.strip() and indent <= box_indent:
            box, box_indent = "", -1
        if found := ADMONITION.match(line):
            box, box_indent = found["title"], len(found["indent"])

        if found := MARKER.match(line):
            marker = (found["kind"], found["arg"])
        elif found := FENCE.match(line):
            closing = found["indent"] + found["ticks"]
            start = i + 1
            i = start
            while i < len(lines) and lines[i].rstrip() != closing:
                i += 1
            code = textwrap.dedent("\n".join(lines[start:i]))
            blocks.append(
                Block(path, start, found["lang"], found["attrs"], code, marker, box)
            )
            marker = None
        elif line.strip():
            marker = None
        i += 1
    return blocks


def check_listing(block: Block, source: str) -> str | None:
    """Return a complaint if the block's pieces aren't in the source, in order."""
    text = "\n".join(line.rstrip() for line in source.splitlines())
    pieces, piece = [], []
    for line in block.code.splitlines():
        if line.strip() == ELISION:
            pieces.append(piece)
            piece = []
        else:
            piece.append(line.rstrip())
    pieces.append(piece)

    position = 0
    for piece in pieces:
        wanted = "\n".join(piece).strip("\n")
        if not wanted:
            continue
        # The chapter may show the inside of a function, which dedent() has
        # shifted left. Try it at each plausible depth of indentation.
        for depth in (0, 4, 8, 12):
            indented = textwrap.indent(wanted, " " * depth)
            found = text.find(indented, position)
            if found >= 0:
                position = found + len(indented)
                break
        else:
            first = wanted.splitlines()[0]
            return f"not found in the file (piece starting {first!r})"
    return None


def run_snippet(code: str) -> str:
    """Run a snippet and return what it printed, plus any error's last line."""
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        try:
            # Running the chapters' own snippets is the whole point of this check.
            exec(compile(code, "<predict>", "exec"), {"__name__": "__predict__"})  # noqa: S102
        except Exception as error:  # noqa: BLE001 - any error is part of the output
            print(f"{type(error).__name__}: {error}")
        finally:
            # A snippet that sets up logging mustn't leave it set up for the next one.
            logging.getLogger().handlers.clear()
            logging.getLogger().setLevel(logging.WARNING)
    return output.getvalue()


def significant(text: str) -> list[str]:
    """The lines that matter when comparing output: not traceback scaffolding."""
    lines = [line.rstrip() for line in text.strip().splitlines()]
    return [ln for ln in lines if not ln.startswith(("Traceback", "  "))]


def project_sources(path: Path) -> list[str]:
    """The src folders of the project a chapter is about: p06-life.md -> projects/06-*/src."""
    found = re.match(r"p(\d\d)-", path.name)
    if not found:
        return []
    return [str(src) for src in (ROOT / "projects").glob(f"{found[1]}-*/src")]


def check_file(path: Path) -> list[str]:
    """Check one chapter, with its own project's packages importable in REPL sessions."""
    sources = project_sources(path)
    before = set(sys.modules)
    sys.path[:0] = sources
    try:
        return check_blocks(path)
    finally:
        del sys.path[: len(sources)]
        for name in set(sys.modules) - before:
            del sys.modules[name]


def check_blocks(path: Path) -> list[str]:
    problems: list[str] = []
    parser = doctest.DocTestParser()
    runner = doctest.DocTestRunner(optionflags=doctest.ELLIPSIS)
    session: dict[str, object] = {"__name__": "__repl__"}
    predicted: Block | None = None

    for block in blocks_in(path):
        kind, arg = block.marker or ("", "")

        if kind == "listing" and arg != "none":
            source = ROOT / arg
            if not source.is_file():
                problems.append(f"{block.where}: no such file as {arg}")
            elif complaint := check_listing(block, source.read_text(encoding="utf-8")):
                problems.append(f"{block.where}: listing of {arg} {complaint}")
        elif block.lang == "python" and "title=" in block.attrs and kind != "listing":
            problems.append(f"{block.where}: titled listing has no listing marker")

        if block.lang == "pycon" and kind != "no-doctest":
            test = parser.get_doctest(block.code, session, block.where, None, 0)
            report = io.StringIO()
            runner.run(test, out=report.write, clear_globs=False)
            # doctest works on a copy of the session; carry its changes forward.
            session.update(test.globs)
            if report.getvalue():
                problems.append(
                    f"{block.where}: REPL session differs\n{report.getvalue()}"
                )

        if block.box == "Predict" and block.lang == "python":
            predicted = None if kind == "no-check" else block
        elif block.box == "Answer" and block.lang == "text" and predicted:
            actual = run_snippet(predicted.code)
            if significant(actual) != significant(block.code):
                problems.append(
                    f"{predicted.where}: Predict snippet prints\n{actual}"
                    f"but the answer at line {block.line} says\n{block.code}\n"
                )
            predicted = None

    return problems


def main() -> None:
    problems: list[str] = []
    count = 0
    for path in sorted(DOCS.rglob("*.md")):
        count += 1
        problems.extend(check_file(path))

    for problem in problems:
        print(problem)
    print(f"{count} pages checked, {len(problems)} problems")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
