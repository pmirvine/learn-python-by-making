"""Stage 1: one second of middle C, as a WAV file, from nothing but arithmetic."""

import wave
from array import array

RATE = 22_050
FREQUENCY = 261.63
LOUDEST = 32_767

period = RATE / FREQUENCY
samples = array("h")
for n in range(RATE):
    high = n % period < period / 2
    samples.append(LOUDEST // 2 if high else -LOUDEST // 2)

data = samples.tobytes()
print(f"{len(samples):,} samples, {len(data):,} bytes")
print("The first eight bytes:", data[:8].hex(" "))

with wave.open("beep.wav", "wb") as file:
    file.setnchannels(1)
    file.setsampwidth(2)
    file.setframerate(RATE)
    file.writeframes(data)
print("Saved beep.wav")
