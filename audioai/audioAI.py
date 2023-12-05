import sounddevice as sd
import numpy as np
import librosa
import joblib

# Function to extract features from real-time audio input
def extract_realtime_features(duration=5, sr=44100):
    print("Listening... (Press Ctrl+C to stop)")
    audio_data = sd.rec(int(duration * sr), samplerate=sr, channels=1, dtype=np.float32)
    sd.wait()

    # Normalize the audio data to the range [-1, 1]
    audio_data /= np.max(np.abs(audio_data), axis=0)

    features = librosa.feature.mfcc(y=audio_data.flatten(), sr=sr, n_mfcc=13)
    return np.mean(features, axis=1)

# Load the pre-trained model
model_filename = "ravdess_emotion_classifier.pkl"
loaded_model = joblib.load(model_filename)

# Function to predict emotion from real-time features
def predict_emotion_from_microphone():
    try:
        # Capture real-time features
        realtime_features = extract_realtime_features()

        # Reshape the features to match the input shape expected by the model
        realtime_features = realtime_features.reshape(1, -1)

        # Make predictions using the pre-trained model
        emotion_prediction = loaded_model.predict(realtime_features)
# Emotion (01 = neutral, 02 = calm, 03 = happy, 04 = sad, 05 = angry, 06 = fearful, 07 = disgust, 08 = surprised).
        emotions = {
            '01':'neutral',
            '02':'calm',
            '03':'happy',
            '04':'sad',
            '05':'angry',
            '06':'fearful',
            '07':'disgust',
            '08':'surprised'
        }
        print("Predicted Emotion:", emotions[emotion_prediction[0]])

    except KeyboardInterrupt:
        print("\nRecording stopped.")

if __name__ == "__main__":
    predict_emotion_from_microphone()
