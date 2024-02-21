import librosa
import numpy as np
import tensorflow as tf

class AudioAI:
    def __init__(self) -> None:
        self.emotion_labels =  ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]
        self.model = tf.keras.models.load_model("audioai/audio_emotion_detection_model.h5")
        
    def predict(self, audio_path):
        
        audio, sr = librosa.load(audio_path, sr=16000)
        features = np.mean(librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40).T, axis=0)
        features = np.expand_dims(features, axis=0)
        features = np.expand_dims(features, axis=2)

        # Predict the emotion
        predictions = self.model.predict(features)
        predicted_emotion = self.emotion_labels[np.argmax(predictions)]

        return predicted_emotion
