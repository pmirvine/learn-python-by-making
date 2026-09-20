# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "rich>=15.0.0",
# ]
# ///

import platform

from rich.console import Console
from rich.panel import Panel


def main() -> None:
    console = Console()
    banner = (
        f"[bold yellow]Python {platform.python_version()} Computer[/]\n\n"
        f"[cyan]{platform.system()} {platform.machine()}[/]\n\n"
        "[green]Ready[/]\n[bold white]>[/][blink]_[/]"
    )
    console.print(Panel(banner, width=44, border_style="red"))


if __name__ == "__main__":
    main()
