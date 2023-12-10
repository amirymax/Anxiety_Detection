import cv2
import numpy as np
from keras.models import model_from_json
from keras.preprocessing.image import img_to_array

class VideoAI:
    def __init__(self) -> None:
        self.labels = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}
        self.model = None
        self.upload_model()
        haar_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(haar_file)
    
    def upload_model(self):
        json_file = open("videoai/facialemotionmodel.json", "r")
        model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(model_json)
        self.model.load_weights("videoai/facialemotionmodel.h5")
    
    def predict(self, path):
        haar_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(haar_file)
        video_capture = cv2.VideoCapture(path)
        output_path = "videoai/video_files/video_output.mp4"

    def extract_features(image):
        feature = img_to_array(image)
        feature = feature.reshape(1, 48, 48, 1)
        return feature / 255.0
 