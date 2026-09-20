import math
import time

MESSAGE = "LEARN PYTHON BY MAKING *** "
WINDOW = 16

for frame in range(240):
    start = frame % len(MESSAGE)
    visible = (MESSAGE * 2)[start : start + WINDOW]
    indent = round(24 + 22 * math.sin(frame / 7))
    colour = 31 + frame // 8 % 6
    print(f"{' ' * indent}\033[1;{colour}m{visible}\033[0m")
    time.sleep(0.04)
