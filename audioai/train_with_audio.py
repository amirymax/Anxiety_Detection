import os
import librosa
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
from time import time
t1 = time()
# Function to extract features from audio files
def extract_features(file_path):
    try:
        audio_data, _ = librosa.load(file_path, sr=None)
        features = librosa.feature.mfcc(y=audio_data, sr=44100, n_mfcc=13)
        return np.mean(features, axis=1)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

# Function to load the RAVDESS dataset
def load_ravdess_dataset(root_dir):
    labels = []
    features = []
    
    for actor_folder in os.listdir(root_dir):
        actor_path = os.path.join(root_dir, actor_folder)
        if os.path.isdir(actor_path):
            for file_name in os.listdir(actor_path):
                file_path = os.path.join(actor_path, file_name)
                if file_path.endswith(".wav"):
                    emotion = file_name.split("-")[2]
                    extracted_features = extract_features(file_path)
                    if extracted_features is not None:
                        print(f'Uploading the {file_name} file')
                        labels.append(emotion)
                        features.append(extracted_features)
    
    return np.array(features), np.array(labels)

# Load the RAVDESS dataset
ravdess_dataset_root = "dataset"
X, y = load_ravdess_dataset(ravdess_dataset_root)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train a RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# Save the trained model as a .pkl file
model_filename = "ravdess_emotion_classifier.pkl"
joblib.dump(model, model_filename)
print(f"Model saved as {model_filename}")

print(f'TIME: {time() - t1}')