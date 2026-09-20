import math
import webbrowser
from pathlib import Path

BIG, SMALL, PEN = 96, 59, 60  # the fixed ring, the rolling wheel, and the pen's hole
TURNS = SMALL // math.gcd(BIG, SMALL)

points = []
for step in range(TURNS * 360 + 1):
    t = math.radians(step)
    across = (BIG - SMALL) * math.cos(t) + PEN * math.cos((BIG - SMALL) / SMALL * t)
    up = (BIG - SMALL) * math.sin(t) - PEN * math.sin((BIG - SMALL) / SMALL * t)
    points.append(f"{across:.1f},{up:.1f}")

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="-100 -100 200 200">
<rect x="-100" y="-100" width="200" height="200" fill="midnightblue"/>
<polyline points="{" ".join(points)}" fill="none" stroke="gold" stroke-width="0.4"/>
</svg>
"""
path = Path("spiro.svg")
path.write_text(svg, encoding="utf-8")
print(f"{len(points):,} points, {len(svg):,} characters, {TURNS} turns of the wheel")
webbrowser.open(path.resolve().as_uri())
