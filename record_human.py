import os
import sounddevice as sd
from scipy.io.wavfile import write

os.makedirs('../data/human', exist_ok=True)

def record_sample(duration=3, sample_rate=16000):
    print(f"Recording {duration} seconds... (Speak now)")
    recording = sd.rec(int(duration * sample_rate),
                     samplerate=sample_rate,
                     channels=1)
    sd.wait()
    return recording

for i in range(50):  # Record 50 samples
    audio = record_sample()
    write(f'../data/human/sample_{i}.wav', 16000, audio)
    print(f"Saved sample_{i}.wav")

print("Human recording complete!")