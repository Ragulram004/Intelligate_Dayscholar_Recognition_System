import streamlit as st
import csv  
import cv2
import os
import numpy as np
import pickle
import face_recognition
import pandas as pd
from datetime import datetime
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, WebRtcMode

# Constants
face_data_file = "face_data.pkl"
root_folder = "FaceDetection"
csv_file = "output/Recordings.csv"
output_dir = "output"
images_dir = "images"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

def train_images():
    all_face_encodings = []
    all_face_names = []

    for class_name in os.listdir(root_folder):
        class_folder = os.path.join(root_folder, class_name)

        if os.path.isdir(class_folder):
            class_face_encodings = []

            for filename in os.listdir(class_folder):
                image_path = os.path.join(class_folder, filename)
                image = face_recognition.load_image_file(image_path)
                face_encodings = face_recognition.face_encodings(image)

                if face_encodings:
                    average_face_encoding = np.mean(face_encodings, axis=0)
                    all_face_encodings.append(average_face_encoding)
                    all_face_names.append(class_name)

    face_data = {'encodings': all_face_encodings, 'names': all_face_names}
    with open(face_data_file, 'wb') as file:
        pickle.dump(face_data, file)

def add_new_class():
    st.subheader("Add New Class and Capture Images")
    class_name = st.text_input("Enter Class Name:")

    if st.button("Add New Class") and class_name:
        folder_path = os.path.join(root_folder, class_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # OpenCV video capture
        video_capture = cv2.VideoCapture(0)
        cv2.namedWindow('Capture Frame')  # Create a window for the frame

        count = 0
        while True:
            ret, frame = video_capture.read()
            frame = cv2.flip(frame, 1)
            cv2.imshow('Capture Frame', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('c'):
                image_path = os.path.join(folder_path, f"{class_name}_{count}.jpg")
                cv2.imwrite(image_path, frame)
                st.success(f"Image {count} captured for class: {class_name}")
                count += 1

            elif key == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

        # Re-train the model after adding new images
        train_images()
        st.success(f"Captured {count} images for class: {class_name}")

def load_face_data():
    if os.path.exists(face_data_file):
        with open(face_data_file, 'rb') as file:
            face_data = pickle.load(file)
            return face_data['encodings'], face_data['names']
    return [], []

class FaceRecognitionTransformer(VideoTransformerBase):
    def __init__(self):
        self.all_face_encodings, self.all_face_names = load_face_data()

    def transform(self, frame):
        image = frame.to_ndarray(format="bgr24")
        face_locations = face_recognition.face_locations(image, model='cnn')  # Use GPU-accelerated CNN model
        face_encodings = face_recognition.face_encodings(image, face_locations)

        detected_names = []

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(self.all_face_encodings, face_encoding, tolerance=0.5)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = self.all_face_names[first_match_index]

            detected_names.append(name)
            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(image, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        if detected_names:
            self.log_detections(detected_names)

        return image

    def log_detections(self, names):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entries = [(name, timestamp) for name in names]

        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(log_entries)

def app():
    st.title("Home")
    add_new_class()  # Add new class form

    # Train Images Button
    if st.button("Train All"):
        train_images()
        st.success("Training completed successfully.")

    # Start Live Face Recognition
    st.subheader("Live Face Recognition")
    webrtc_streamer(key="example", mode=WebRtcMode.SENDRECV, video_transformer_factory=FaceRecognitionTransformer)
