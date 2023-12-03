import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint
from PIL import Image
import os

# Function to load images from a directory and label them
def load_images_from_directory(directory):
    labels = []
    images = []

    for label_id, emotion in enumerate(emotion_classes):
        emotion_directory = os.path.join(directory, emotion)
        for filename in os.listdir(emotion_directory):
            if filename.endswith(".jpg"):
                labels.append(label_id)
                img_path = os.path.join(emotion_directory, filename)
                img = Image.open(img_path).convert('L')  # Open image in grayscale mode
                img_array = np.array(img)
                images.append(img_array)

    return np.array(images), np.array(labels)

# Define emotion classes
emotion_classes = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

# Load training data
X_train, y_train = load_images_from_directory('videoai/fer2013/train')

# Load validation data
X_val, y_val = load_images_from_directory('videoai/fer2013/test')

# Create a simple CNN model
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(len(emotion_classes), activation='softmax')  # Output layer with the number of classes
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Data augmentation to improve generalization
datagen = ImageDataGenerator(rotation_range=20, width_shift_range=0.2, height_shift_range=0.2, horizontal_flip=True)
datagen.fit(X_train.reshape(-1, 48, 48, 1))  # Reshape for data augmentation

# ModelCheckpoint to save the best model during training
checkpoint = ModelCheckpoint('videoai/fer2013_model.h5', save_best_only=True)

# Train the model
history = model.fit(datagen.flow(X_train.reshape(-1, 48, 48, 1), y_train, batch_size=64),
                    validation_data=(X_val.reshape(-1, 48, 48, 1), y_val),
                    epochs=20, callbacks=[checkpoint])

# Save the model using pickle
with open('videoai/fer2013_model.pkl', 'wb') as file:
    pickle.dump(model, file)
