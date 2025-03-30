import sounddevice as sd
import librosa
import numpy as np
import joblib
from colorama import init, Fore
import time  # Added missing import

# Initialize colors
init()
HUMAN_COLOR = Fore.GREEN
BOT_COLOR = Fore.RED
UNCERTAIN_COLOR = Fore.YELLOW

# Load model
model = joblib.load('../models/voice_classifier.pkl')

# Settings
SAMPLE_RATE = 16000
DURATION = 3  # Recording duration
SILENCE_THRESHOLD = 0.02  # Adjust based on your mic


def extract_features(audio):
    """Extract only MFCC features (13 features)"""
    mfccs = librosa.feature.mfcc(
        y=audio,
        sr=SAMPLE_RATE,
        n_mfcc=13,
        hop_length=512
    )
    return np.mean(mfccs.T, axis=0)  # Only return mean of MFCCs (13 features)


def analyze_voice(audio):
    """Classify voice with confidence"""
    features = extract_features(audio)
    human_prob = model.predict_proba([features])[0][0]
    return human_prob


def record_audio():
    """Record audio chunk with verification"""
    print("\n" + "=" * 40)
    print("Recording... (Speak clearly)")
    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        blocking=True
    ).flatten()

    # Check audio quality
    max_amp = np.max(np.abs(audio))
    if max_amp < SILENCE_THRESHOLD:
        print(UNCERTAIN_COLOR + ">>> Too quiet. Try again." + Fore.RESET)
        return None
    return audio


def main():
    print(f"\n{Fore.CYAN}=== AI/Human Voice Detector ===")
    print(f"• {HUMAN_COLOR}Human detection threshold: >85% confidence")
    print(f"• {BOT_COLOR}AI detection threshold: <15% confidence{Fore.RESET}")
    print("• Recording duration:", DURATION, "seconds")
    print("=" * 40)

    while True:
        audio = record_audio()
        if audio is None:
            continue

        human_prob = analyze_voice(audio)

        if human_prob > 0.85:
            print(HUMAN_COLOR + f">>> HUMAN VOICE ({human_prob:.2%} confidence)" + Fore.RESET)
        elif human_prob < 0.15:
            print(BOT_COLOR + f">>> AI-GENERATED VOICE ({1 - human_prob:.2%} confidence)" + Fore.RESET)
        else:
            print(UNCERTAIN_COLOR + ">>> UNCERTAIN (Try speaking clearly)" + Fore.RESET)

        print("\nPress Ctrl+C to exit or wait for next recording...")
        time.sleep(1)  # Brief pause between detections


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RESET + "\nDetection stopped.")