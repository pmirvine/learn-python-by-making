"""Build the site: read the articles, and write a folder of web pages."""

import argparse
import shutil
from datetime import datetime
from importlib.resources import files
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape

from pyfax import mosaic
from pyfax.content import ContentError, pages
from pyfax.page import Cell, Colour, Page


def classes(cell: Cell) -> str:
    """Return the CSS classes for a cell: its ink, its paper, and any graphics."""
    names = [f"i{cell.ink.value}", f"p{cell.paper.value}"]
    if cell.dots:
        names += ["m", f"m{cell.dots}"]
    return " ".join(names)


def environment() -> Environment:
    env = Environment(
        loader=PackageLoader("pyfax"),
        autoescape=select_autoescape(),
        trim_blocks=True,
    )
    env.filters["classes"] = classes
    return env


def stylesheet() -> str:
    """Return the whole stylesheet: the part that's written by hand, and the rest."""
    written = (files("pyfax") / "static" / "style.css").read_text(encoding="utf-8")
    colours = "".join(
        f".i{colour.value} {{ color: {colour.css}; }}\n"
        f".p{colour.value} {{ background-color: {colour.css}; }}\n"
        for colour in Colour
    )
    return f"{written}\n{colours}\n{mosaic.stylesheet()}"


def write_site(site: list[Page], out: Path) -> None:
    """Write a page of HTML for every page, and the files that they all share."""
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    template = environment().get_template("page.html")
    for page in site:
        html = template.render(page=page)
        (out / f"{page.number}.html").write_text(html, encoding="utf-8")
    shutil.copy(out / f"{site[0].number}.html", out / "index.html")
    (out / "style.css").write_text(stylesheet(), encoding="utf-8")
    script = (files("pyfax") / "static" / "pyfax.js").read_text(encoding="utf-8")
    (out / "pyfax.js").write_text(script, encoding="utf-8")
    missing = out / "404.html"
    lost = Page(404, "No such page")
    lost.write(12, 8, "There's no such page.", Colour.YELLOW)
    lost.write(14, 8, "Try the index: 100", Colour.CYAN, link=100)
    missing.write_text(template.render(page=lost), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("content", nargs="?", type=Path, default=Path("content"))
    parser.add_argument("--out", type=Path, default=Path("site"))
    args = parser.parse_args()

    try:
        today = datetime.now().astimezone().date()  # the date here, wherever here is
        site = pages(args.content, today)
    except (OSError, ContentError) as error:
        raise SystemExit(f"Can't build the site: {error}") from error
    write_site(site, args.out)
    print(f"Wrote {len(site)} pages to {args.out}/")
