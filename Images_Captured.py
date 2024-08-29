import streamlit as st
from PIL import Image
import os

def load_images():
    images_dir = "images"
    image_files = os.listdir(images_dir)
    return [os.path.join(images_dir, img_file) for img_file in image_files]

def app():
    st.title("Image Captured")
    images = load_images()

    search_term = st.text_input("Search by Image Name:")
    filtered_images = [img for img in images if search_term.lower() in img.lower()]

    if filtered_images:
        columns = st.columns(4)
        for img_path in filtered_images:
            img = Image.open(img_path)
            columns[filtered_images.index(img_path) % 4].image(img, use_column_width=True, caption=os.path.basename(img_path))
    else:
        st.warning("No images found matching the search criteria.")
