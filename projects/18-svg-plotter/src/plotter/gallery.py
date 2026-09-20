"""Show a folder of pictures as a web page, served from your own machine."""

import argparse
import webbrowser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from plotter.markup import render

STYLE = """
body { background: #111; color: #eee; font-family: system-ui, sans-serif; margin: 2rem; }
main { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1rem; }
figure { margin: 0; }
img { width: 100%; border: 1px solid #444; }
figcaption { text-align: center; padding: 0.5rem; }
"""


def page(folder: Path) -> str:
    """Return a page of HTML with every SVG file in the folder on it."""
    pictures = sorted(folder.glob("*.svg"))
    figures = [
        t'<figure><img src="{picture.name}" alt="{picture.stem}">'
        t"<figcaption>{picture.stem}</figcaption></figure>\n"
        for picture in pictures
    ]
    return render(
        t"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{folder.resolve().name}: {len(pictures)} pictures</title>
<style>{STYLE}</style>
</head>
<body>
<h1>{folder.resolve().name}</h1>
<main>
{figures}</main>
</body>
</html>
"""
    )


def server_for(folder: Path, port: int) -> ThreadingHTTPServer:
    """Return a web server that serves the files in a folder, to this machine only."""
    handler = partial(SimpleHTTPRequestHandler, directory=str(folder))
    return ThreadingHTTPServer(("127.0.0.1", port), handler)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", nargs="?", type=Path, default=Path("pictures"))
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()

    if not args.folder.is_dir():
        raise SystemExit(f"There's no folder called {args.folder}")
    (args.folder / "index.html").write_text(page(args.folder), encoding="utf-8")

    with server_for(args.folder, args.port) as server:
        address = f"http://127.0.0.1:{server.server_port}/"
        print(f"Serving {args.folder} at {address}  (Ctrl+C to stop)")
        if not args.no_browser:
            webbrowser.open(address)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")
