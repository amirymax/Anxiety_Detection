import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import sounddevice as sd
import librosa
import joblib
import random
import pickle 

# Function to extract features from audio data
def extract_features(audio_data, sample_rate):
    mfccs = librosa.feature.mfcc(y=audio_data.astype(float), sr=sample_rate, n_mfcc=13)
    return np.mean(mfccs.T, axis=0)

# Load the saved model and scaler
model_filename = 'audioai/audio_emotion_detection_model.pkl'
with open(model_filename, 'rb') as model_file:
    model = pickle.load(model_file)
scaler_filename = 'audioai/emotion_classifier_scaler.pkl'
scaler = joblib.load(scaler_filename)

# Reverse mapping for emotion labels
emotion_labels_reverse = {0: 'ANG', 1: 'DIS', 2: 'FEA', 3: 'HAP', 4: 'NEU', 5: 'SAD'}

# Function to classify emotion from audio data
def classify_emotion(audio_data, sample_rate):
    features = extract_features(audio_data, sample_rate)
    features_scaled = scaler.transform([features])
    prediction = model.predict(features_scaled)[0]
    predicted_class = np.argmax(prediction)
    return predicted_class

# Record audio for a specific duration
def record_audio(duration, sample_rate):
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()
    return np.squeeze(recording)

# Set up the microphone input
sample_rate = 16000
channels = 1
duration = 5  # Set the duration for recording (in seconds)

# Record audio
print(f'Recording for {duration} seconds...')
audio_data = record_audio(duration, sample_rate)

# Classify emotion
prediction = classify_emotion(audio_data, sample_rate)
predicted_emotion = emotion_labels_reverse[prediction]

print(f'Predicted Emotion: {predicted_emotion}')
