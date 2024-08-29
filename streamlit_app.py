import os
import cv2
import streamlit as st
import numpy as np
import pickle
import face_recognition
import datetime
import csv
from PIL import Image
import pandas as pd

# Constants
face_data_file = "face_data.pkl"
root_folder = "FaceDetection"
csv_file = "Recordings.csv"  # Specify the path for the CSV file here

# Directory to save the CSV file
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

csv_file = os.path.join(output_dir, csv_file)  # Construct the full path for the CSV file

# Directory to save captured images
images_dir = "images"
os.makedirs(images_dir, exist_ok=True)  # Create the directory if it doesn't exist

# Global dictionary to keep track of the last detection time for each class
last_detection_times = {}

# Function to load face data from pickle file
def load_face_data():
    if not os.path.exists(face_data_file):
        st.error("No face data found. Please train the system first.")
        return [], []

    with open(face_data_file, 'rb') as file:
        face_data = pickle.load(file)
        all_face_encodings = face_data.get('encodings', [])
        all_face_names = face_data.get('names', [])

    return all_face_encodings, all_face_names

# Function to train images and update face data
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

# Function to recognize faces in a given frame
def recognize_faces(frame, all_face_encodings, all_face_names):
    global last_detection_times

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(all_face_encodings, face_encoding, tolerance=0.5)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = all_face_names[first_match_index]

            # Always draw rectangle and display the name
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Get the current time
            current_time = datetime.datetime.now()
            current_minute = current_time.replace(second=0, microsecond=0)

            # Check if this person was detected within the current minute
            if name in last_detection_times:
                if last_detection_times[name] == current_minute:
                    continue  # Skip logging and capturing if already done this minute

            # Log detection in CSV file
            detection_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            with open(csv_file, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([name, detection_time])

            # Update the last detection time for this person
            last_detection_times[name] = current_minute

            # Save the captured image with timestamp as filename
            image_filename = os.path.join(images_dir, f"{name}{current_time.strftime('%Y-%m-%d%H-%M-%S')}.jpeg")
            print("Image filename:", image_filename)
            cv2.imwrite(image_filename, frame)

    return frame

# Function to load images from the 'images' directory
def load_images():
    image_files = os.listdir(images_dir)
    image_files.sort()
    return [os.path.join(images_dir, img_file) for img_file in image_files]

# Function to add a new class (person) and capture images using OpenCV
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

# Main Streamlit app
def main():
    st.title("Face Recognition App")

    # Sidebar navigation
    mode = st.sidebar.selectbox("Navigation", ("Home", "User Log", "Image Captured"))

    if mode == "Home":
        add_new_class()  # Call the function to add a new class

        # Train Images
        if st.button("Train All"):
            train_images()
            st.success("Training completed successfully.")

        # Live Face Recognition
        if st.button("Start Live Face Recognition"):
            video_feed = st.empty()
            video_capture = cv2.VideoCapture(0)

            while True:
                ret, frame = video_capture.read()
                if not ret:
                    st.error("Error reading frame from webcam.")
                    break

                processed_frame = recognize_faces(frame, *load_face_data())

                video_feed.image(cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB), channels="RGB")

    elif mode == "User Log":
        st.subheader("User Log - Detection Logs")

        # Display Detection Log
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file, names=["Name", "Detection Time"])
            st.dataframe(df)
        else:
            st.warning("No detection log found.")

    elif mode == "Image Captured":
        st.subheader("Dayscholars Captured")

        image_files = load_images()
        search_term = st.text_input("Search by Image Name:")
        filtered_images = [img for img in image_files if search_term.lower() in img.lower()]

        if filtered_images:
            columns = st.columns(4)
            for img_path in filtered_images:
                img = Image.open(img_path)
                columns[filtered_images.index(img_path) % 4].image(img, use_column_width=True, caption=os.path.basename(img_path))
        else:
            st.warning("No images found matching the search criteria.")

if __name__ == "__main__":
    main()
