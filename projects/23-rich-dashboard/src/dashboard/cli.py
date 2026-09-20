"""How your projects are getting on: a dashboard in the terminal."""

import argparse
import time
from datetime import UTC, datetime
from pathlib import Path

from rich.console import Console, RenderableType
from rich.live import Live
from rich.progress import track

from dashboard.stats import find_projects, scan
from dashboard.view import SORTS, dashboard


def build(
    root: Path, order: str, weeks: int, console: Console | None
) -> RenderableType:
    """Scan every project under a folder, and return the display."""
    folders = find_projects(root)
    if console is not None:
        folders = track(
            folders, description="Scanning", console=console, transient=True
        )
    projects = [scan(folder) for folder in folders]
    return dashboard(projects, datetime.now(UTC), order, weeks)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--sort", choices=sorted(SORTS), default="name")
    parser.add_argument("--weeks", type=int, default=12)
    parser.add_argument("--watch", type=float, metavar="SECONDS", help="keep looking")
    args = parser.parse_args()

    console = Console()
    if not args.watch:
        console.print(build(args.root, args.sort, args.weeks, console))
        return

    with Live(build(args.root, args.sort, args.weeks, None), console=console) as live:
        try:
            while True:
                time.sleep(args.watch)
                live.update(build(args.root, args.sort, args.weeks, None))
        except KeyboardInterrupt:
            pass
