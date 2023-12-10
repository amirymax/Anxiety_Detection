import cv2
import numpy as np
from keras.models import model_from_json
from keras.preprocessing.image import img_to_array

json_file = open("videoai/facialemotionmodel.json", "r")
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)

model.load_weights("videoai/facialemotionmodel.h5")

haar_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(haar_file)

def extract_features(image):
    feature = img_to_array(image)
    feature = feature.reshape(1, 48, 48, 1)
    return feature / 255.0

video_path = "videoai/video_files/file.MOV"
video_capture = cv2.VideoCapture(video_path)

labels = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}

# Set the output file path and properties
output_path = "videoai/video_files/video_output.mp4"
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_video = cv2.VideoWriter(output_path, fourcc, 30.0, (int(video_capture.get(3)), int(video_capture.get(4))))
while True:
    ret, im = video_capture.read()
    if not ret:
        break

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(im, 1.3, 5)

    try:
        for (p, q, r, s) in faces:
            face_image = gray[q:q + s, p:p + r]
            cv2.rectangle(im, (p, q), (p + r, q + s), (255, 0, 0), 2)
            face_image = cv2.resize(face_image, (48, 48))
            img = extract_features(face_image)
            pred = model.predict(img)
            prediction_label = labels[pred.argmax()]

            # Print the emotion in the terminal
            print("Emotion:", prediction_label)

        # Write the frame to the output video file
        output_video.write(im)

    except cv2.error:
        pass

# Release the video capture and writer objects
video_capture.release()
output_video.release()
