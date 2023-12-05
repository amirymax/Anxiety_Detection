import sounddevice as sd
import numpy as np
import librosa
import joblib
class AudioAI:
    def __init__(self) -> None:
        model_filename = 'audioai/audio_emotion_detection_model.pkl'        
        self.loaded_model = joblib.load(model_filename)
        
    def listen(self):
        duration=5
        sr=44100
        print("Listening... (Press Ctrl+C to stop)")
        audio_data = sd.rec(int(duration * sr), samplerate=sr, channels=1, dtype=np.float32)
        sd.wait()

        # Normalize the audio data to the range [-1, 1]
        audio_data /= np.max(np.abs(audio_data), axis=0)

        features = librosa.feature.mfcc(y=audio_data.flatten(), sr=sr, n_mfcc=13)
        return np.mean(features, axis=1)

    def predict(self):
        try:
        # Capture real-time features
            realtime_features = self.listen()

            # Reshape the features to match the input shape expected by the model
            realtime_features = realtime_features.reshape(1, -1)

            # Make predictions using the pre-trained model
            emotion_prediction = self.loaded_model.predict(realtime_features)
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



model = AudioAI()
model.predict()