"""The `micro` command."""

import argparse
from importlib import resources
from importlib.metadata import version
from pathlib import Path

from micro.computer import Micro


def stock(disc: Path) -> None:
    """Put the welcome programs on the disc, unless they're there already.

    They travel inside the package, and so they're wherever the package is installed.
    """
    disc.mkdir(parents=True, exist_ok=True)
    for item in resources.files("micro").joinpath("welcome").iterdir():
        if not (disc / item.name).exists():
            (disc / item.name).write_bytes(item.read_bytes())


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="micro", description="A computer that boots to BASIC."
    )
    parser.add_argument(
        "disc", nargs="?", type=Path, default=Path("disc"), help="a folder"
    )
    parser.add_argument(
        "--version", action="version", version=f"micro {version('micro')}"
    )
    args = parser.parse_args()
    stock(args.disc)
    Micro(args.disc).run()
