import os
import librosa
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

def extract_features(file_path):
    try:
        audio, sr = librosa.load(file_path, sr=16000)
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
        return np.mean(mfccs.T, axis=0)
    except:
        return None

X, y = [], []

print("Processing human samples...")
for file in os.listdir('../data/human'):
    if file.endswith('.wav'):
        features = extract_features(f'../data/human/{file}')
        if features is not None:
            X.append(features)
            y.append(0)

print("Processing bot samples...")
for file in os.listdir('../data/bot'):
    if file.endswith('.wav'):
        features = extract_features(f'../data/bot/{file}')
        if features is not None:
            X.append(features)
            y.append(1)

X, y = np.array(X), np.array(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier(
    n_estimators=200,
    class_weight={0:1, 1:2},  # Higher weight for bot detection
    max_depth=7
)
model.fit(X_train, y_train)

print("\n=== Evaluation ===")
print(classification_report(y_test, model.predict(X_test)))

os.makedirs('../models', exist_ok=True)
joblib.dump(model, '../models/voice_classifier.pkl')
print("\nModel saved to models/voice_classifier.pkl")