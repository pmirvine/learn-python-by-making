"""Put the page and the life package together in one folder, ready to be served.

uv run make_site.py
uv run python -m http.server --directory site
"""

import shutil
from pathlib import Path

HERE = Path(__file__).parent
LIFE = HERE.parent / "06-life" / "src" / "life"
SITE = Path("site")

if SITE.exists():
    shutil.rmtree(SITE)
shutil.copytree(HERE / "life-in-a-tab", SITE)
shutil.copytree(
    LIFE, SITE / "life", ignore=shutil.ignore_patterns("__pycache__", "cli.py")
)
print(f"Made {SITE}/, with {len(list(SITE.rglob('*')))} files in it.")
