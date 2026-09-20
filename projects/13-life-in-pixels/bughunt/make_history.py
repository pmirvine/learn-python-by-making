"""Build a small Git repository with a bug hidden in its history, to practise bisecting.

    uv run bughunt/make_history.py            # makes ./bisect-practice
    uv run bughunt/make_history.py somewhere  # or put it somewhere else

A colleague has spent a fortnight improving a little camera module, in fourteen
commits. The first commit is tagged v0.1, and it worked. The last one doesn't:
clicking anywhere to the left of the origin, or above it, paints the wrong cell.
"""

import os
import subprocess
import sys
from pathlib import Path

START = '''"""Where things are on the screen."""

import math

ZOOM = 8


def cell_at(px, py, left=0, top=0):
    """Return the cell under a pixel."""
    return math.floor(left + px / ZOOM), math.floor(top + py / ZOOM)
'''

# Each commit: a message, some text to find in camera.py, and what to put in its place.
COMMITS = [
    (
        "Add pixel_of, the way back from a cell to a pixel",
        "    return math.floor(left + px / ZOOM), math.floor(top + py / ZOOM)\n",
        (
            "    return math.floor(left + px / ZOOM), math.floor(top + py / ZOOM)\n"
            "\n\ndef pixel_of(cx, cy, left=0, top=0):\n"
            '    """Return the pixel at the corner of a cell."""\n'
            "    return round((cx - left) * ZOOM), round((cy - top) * ZOOM)\n"
        ),
    ),
    ("Say what the zoom is", "ZOOM = 8\n", "ZOOM = 8  # pixels to a cell\n"),
    (
        "Add panned, for dragging the view about",
        "\n\ndef pixel_of(",
        (
            "\n\ndef panned(left, top, dx, dy):\n"
            '    """Return where the corner of the view goes, after a drag."""\n'
            "    return left - dx / ZOOM, top - dy / ZOOM\n"
            "\n\ndef pixel_of("
        ),
    ),
    ("Call the corner x and y, as everybody else does", "left", "x"),
    ("And top becomes y", "top", "y"),
    (
        "Add limits for the zoom",
        "ZOOM = 8  # pixels to a cell\n",
        "ZOOM = 8  # pixels to a cell\nMIN_ZOOM, MAX_ZOOM = 1, 64\n",
    ),
    (
        "Tidy a docstring",
        "Return the cell under a pixel.",
        "Return the cell that's under a pixel.",
    ),
    (
        "Simplify cell_at",
        "    return math.floor(x + px / ZOOM), math.floor(y + py / ZOOM)\n",
        "    return int(x + px / ZOOM), int(y + py / ZOOM)\n",
    ),
    (
        "Add clamped, to keep the zoom within its limits",
        "\n\ndef cell_at(",
        (
            "\n\ndef clamped(zoom):\n"
            '    """Return the zoom, brought within its limits."""\n'
            "    return max(MIN_ZOOM, min(MAX_ZOOM, zoom))\n"
            "\n\ndef cell_at("
        ),
    ),
    (
        "Let the caller choose the zoom",
        "def cell_at(px, py, x=0, y=0):",
        "def cell_at(px, py, x=0, y=0, zoom=ZOOM):",
    ),
    (
        "Use the caller's zoom",
        "int(x + px / ZOOM), int(y + py / ZOOM)",
        "int(x + px / zoom), int(y + py / zoom)",
    ),
    ("Remove an import that nothing uses any more", "import math\n\n", ""),
    (
        "Describe the module properly",
        '"""Where things are on the screen."""',
        '"""Where things are on the screen: converting between pixels and cells."""',
    ),
]


def git(repo: Path, *arguments: str, day: int = 1) -> None:
    """Run a Git command in the practice repository, as a colleague, on a given day."""
    stamp = f"2026-03-{day:02}T10:00:00+00:00"
    identity = {
        "GIT_AUTHOR_NAME": "A. Colleague",
        "GIT_AUTHOR_EMAIL": "colleague@example.com",
        "GIT_AUTHOR_DATE": stamp,
        "GIT_COMMITTER_NAME": "A. Colleague",
        "GIT_COMMITTER_EMAIL": "colleague@example.com",
        "GIT_COMMITTER_DATE": stamp,
    }
    subprocess.run(
        ["git", "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false", *arguments],
        cwd=repo,
        env=os.environ | identity,
        check=True,
        capture_output=True,
    )


def main() -> None:
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else "bisect-practice")
    if repo.exists():
        raise SystemExit(
            f"{repo} is there already. Delete it first, or choose another name."
        )
    repo.mkdir(parents=True)
    camera = repo / "camera.py"

    git(repo, "init", "--quiet", "--initial-branch=main")
    camera.write_text(START, encoding="utf-8", newline="\n")
    git(repo, "add", "camera.py")
    git(repo, "commit", "--quiet", "-m", "Start the camera module")
    git(repo, "tag", "v0.1")

    for day, (message, old, new) in enumerate(COMMITS, start=2):
        text = camera.read_text(encoding="utf-8")
        if old not in text:
            raise SystemExit(f"Can't make the commit {message!r}: {old!r} isn't there.")
        camera.write_text(text.replace(old, new), encoding="utf-8", newline="\n")
        git(repo, "commit", "--quiet", "-am", message, day=day)

    print(f"Made {repo}, with {len(COMMITS) + 1} commits. The first is tagged v0.1.")


if __name__ == "__main__":
    main()
