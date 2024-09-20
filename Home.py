import streamlit as st
import csv  
import cv2
import os
import numpy as np
import pickle
import face_recognition
from datetime import datetime

# Constants
face_data_file = "face_data.pkl"
root_folder = "FaceDetection"
csv_file = "output/Recordings.csv"
output_dir = "output"
images_dir = "images"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)
os.makedirs(images_dir, exist_ok=True)  # Ensure images directory exists

def train_images():
    all_face_encodings = []
    all_face_names = []

    for class_name in os.listdir(root_folder):
        class_folder = os.path.join(root_folder, class_name)

        if os.path.isdir(class_folder):
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

# Initialize a global dictionary to track the last log time for each person
last_logged_times = {}

def log_detections(names, frame):
    global last_logged_times
    current_time = datetime.now()
    log_entries = []

    for name in names:
        if name not in last_logged_times:
            # Log the detection and capture image if the person hasn't been logged before
            log_entries.append((name, current_time.strftime("%Y-%m-%d %H:%M:%S")))
            last_logged_times[name] = current_time

            # Save captured image with a timestamp
            image_filename = os.path.join(images_dir, f"{name}_{current_time.strftime('%Y-%m-%d_%H-%M-%S')}.jpeg")
            cv2.imwrite(image_filename, frame)
            st.write(f"Captured image for {name}: {image_filename}")
        else:
            # Check if the last log for this person was more than 1 minute ago
            time_diff = (current_time - last_logged_times[name]).total_seconds() / 60.0
            if time_diff >= 1:  # Only log if more than 1 minute has passed
                log_entries.append((name, current_time.strftime("%Y-%m-%d %H:%M:%S")))
                last_logged_times[name] = current_time

                # Save captured image with a timestamp
                image_filename = os.path.join(images_dir, f"{name}_{current_time.strftime('%Y-%m-%d_%H-%M-%S')}.jpeg")
                cv2.imwrite(image_filename, frame)
                st.write(f"Captured image for {name}: {image_filename}")

    # Write the log entries immediately after detection
    if log_entries:
        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(log_entries)

def start_live_face_recognition():
    st.subheader("Live Face Recognition (via OpenCV)")

    # Load face data
    all_face_encodings, all_face_names = load_face_data()

    if len(all_face_encodings) == 0:
        st.warning("No face data found. Please train the model first.")
        return

    # OpenCV video capture
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        st.error("Error opening webcam.")
        return

    # Start the live video feed and face recognition
    while True:
        ret, frame = video_capture.read()
        if not ret:
            st.error("Failed to read frame from webcam.")
            break

        # Flip the frame (optional)
        frame = cv2.flip(frame, 1)

        # Detect face locations and encodings
        face_locations = face_recognition.face_locations(frame, model='cnn')  # Use GPU-accelerated CNN model
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        detected_names = []

        # Iterate through detected faces
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(all_face_encodings, face_encoding, tolerance=0.5)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = all_face_names[first_match_index]

            # Draw rectangle around face and put the name
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            detected_names.append(name)

        # Display the resulting frame
        cv2.imshow('Live Face Recognition', frame)

        # Log and capture images
        if detected_names:
            log_detections(detected_names, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

def app():
    st.title("Home")
    add_new_class()  # Add new class form

    # Train Images Button
    if st.button("Train All"):
        train_images()
        st.success("Training completed successfully.")

    # Start Live Face Recognition
    if st.button("Start Live Face Recognition"):
        start_live_face_recognition()
