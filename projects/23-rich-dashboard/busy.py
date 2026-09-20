"""When do you work? A chart of this repository's commits, by the hour of the day."""

import subprocess
from collections import Counter
from datetime import datetime

printed = subprocess.run(
    ["git", "log", "--format=%aI"], capture_output=True, text=True, check=True
).stdout
times = [datetime.fromisoformat(line) for line in printed.splitlines()]
hours = Counter(time.hour for time in times)
days = Counter(f"{time:%a}" for time in times)

tallest = max(hours.values(), default=1)
for hour in range(24):
    bar = "█" * round(40 * hours[hour] / tallest)
    print(f"{hour:02}:00 {bar} {hours[hour] or ''}")

print()
print("  ".join(f"{day} {count}" for day, count in days.most_common()))
if times:
    span = max(times) - min(times)
    print(f"{len(times)} commits in {span.days + 1} days, since {min(times):%d %B %Y}")
