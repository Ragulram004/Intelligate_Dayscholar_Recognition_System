import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
USERNAME = os.getenv("ID")
PASSWORD = os.getenv("PASSWORD")

def app():
    st.title("Login Page")

    # Create text inputs for username and password
    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")

    # Create a login button
    if st.button("Login"):
        if username_input == USERNAME and password_input == PASSWORD:
            st.success(f"Welcome {username_input}!")
            return True  # Return True if login is successful
        else:
            st.error("Username/password is incorrect")

    return False  # Return False if login fails
