"""Print one version's section of CHANGELOG.md: the notes for its release.

uv run scripts/notes.py 1.0.0
"""

import re
import sys
from pathlib import Path

CHANGELOG = Path(__file__).parent.parent / "CHANGELOG.md"


def sections(changelog: str) -> dict[str, str]:
    """Return what the changelog says about each version, newest first."""
    body = re.split(r"^\[[^\]]+\]: ", changelog, maxsplit=1, flags=re.MULTILINE)[0]
    found: dict[str, str] = {}
    for section in re.split(r"^## ", body, flags=re.MULTILINE)[1:]:
        heading, _, text = section.partition("\n")
        if match := re.match(r"\[(?P<version>[^\]]+)\]", heading):
            found[match["version"]] = text.strip()
    return found


def main() -> None:
    known = sections(CHANGELOG.read_text(encoding="utf-8"))
    match sys.argv[1:]:
        case [version] if version in known:
            print(known[version])
        case [version]:
            raise SystemExit(f"CHANGELOG.md says nothing about {version}.")
        case _:
            raise SystemExit("Usage: notes.py VERSION")


if __name__ == "__main__":
    main()
