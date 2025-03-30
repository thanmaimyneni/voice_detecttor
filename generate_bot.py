import os
import wave
import numpy as np
from gtts import gTTS
import io
import subprocess

os.makedirs('../data/bot', exist_ok=True)


def generate_silent_wav(duration=3, sample_rate=16000, filename='output.wav'):
    """Generate a silent WAV file with proper headers"""
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b'\x00' * int(duration * sample_rate * 2))


def text_to_speech(text, filename):
    """Generate speech and save as WAV without FFmpeg"""
    try:
        # Generate speech to memory
        tts = gTTS(text=text, lang='en')
        mp3_data = io.BytesIO()
        tts.write_to_fp(mp3_data)
        mp3_data.seek(0)

        # Create placeholder WAV (actual TTS requires FFmpeg)
        generate_silent_wav(filename=filename)
        print(f"Generated placeholder: {filename}")

    except Exception as e:
        print(f"Error generating {filename}: {str(e)}")
        generate_silent_wav(filename=filename)  # Fallback to silent audio


# Sample texts
text_samples = [
    "This is a synthetic voice sample",
    "Text to speech without FFmpeg",
    "Voice bot detection experiment"
]

# Generate 50 samples
for i in range(50):
    text = text_samples[i % len(text_samples)]
    wav_path = f'../data/bot/bot_sample_{i}.wav'
    text_to_speech(text, wav_path)

print("\nGenerated 50 placeholder WAV files in ../data/bot/")
print("Note: These are silent files. For real TTS, install FFmpeg.")