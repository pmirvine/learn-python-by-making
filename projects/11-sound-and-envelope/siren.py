import math
import wave
from array import array

RATE = 22_050
SECONDS = 4

samples = array("h")
phase = 0.0
for n in range(RATE * SECONDS):
    wail = math.sin(math.tau * n / RATE * 0.5)
    frequency = 700 + 300 * wail
    phase += math.tau * frequency / RATE
    samples.append(int(20_000 * math.sin(phase)))

with wave.open("siren.wav", "wb") as file:
    file.setnchannels(1)
    file.setsampwidth(2)
    file.setframerate(RATE)
    file.writeframes(samples.tobytes())

print(f"Saved siren.wav: {len(samples):,} samples, {len(samples.tobytes()):,} bytes")
