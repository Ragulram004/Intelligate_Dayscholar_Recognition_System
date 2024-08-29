import streamlit as st

def authenticate(username, password):
    # Hardcoded username and password for demonstration purposes
    if username == "user" and password == "password":
        return True
    else:
        return False

def app():
    st.title("Login")

    # Define input fields for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Check if the login button is clicked
    if st.button("Login"):
        if authenticate(username, password):
            # Set session state to indicate user is logged in
            st.session_state.is_logged_in = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password. Please try again.")
