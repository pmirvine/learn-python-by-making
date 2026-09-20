import threading
import urllib.request
from pathlib import Path

from plotter import Plot
from plotter.gallery import page, server_for


def make_pictures(folder: Path) -> None:
    for name in ("b & w", "aardvark"):
        with Plot(folder / f"{name}.svg") as plot:
            plot.draw(100, 100)


def test_the_page_lists_the_pictures_in_order_with_their_names_escaped(tmp_path):
    make_pictures(tmp_path)
    html = page(tmp_path)
    assert html.index("aardvark.svg") < html.index("b &amp; w.svg")
    assert "<figcaption>b &amp; w</figcaption>" in html
    assert "2 pictures" in html


def test_the_server_serves_the_folder(tmp_path):
    make_pictures(tmp_path)
    (tmp_path / "index.html").write_text(page(tmp_path), encoding="utf-8")
    with server_for(tmp_path, port=0) as server:
        threading.Thread(target=server.serve_forever, daemon=True).start()
        address = f"http://127.0.0.1:{server.server_port}"
        with urllib.request.urlopen(f"{address}/") as reply:
            assert reply.status == 200
            assert "<h1>" in reply.read().decode()
        with urllib.request.urlopen(f"{address}/aardvark.svg") as reply:
            assert reply.headers["Content-Type"] == "image/svg+xml"
        server.shutdown()
