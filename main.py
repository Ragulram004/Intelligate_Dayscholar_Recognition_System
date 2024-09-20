import streamlit as st
from streamlit_option_menu import option_menu
from login import app as login_app
import Home, User_logs, Images_Captured, About

# Set page configuration
st.set_page_config(page_title="Intelligate")

# Check login status
is_logged_in = login_app()

if is_logged_in:
    class MultiApp:
        def __init__(self):
            self.apps = []

        def add_app(self, title, func):
            self.apps.append({
                "title": title,
                "function": func
            })

        def run(self):
            app = option_menu(
                menu_title=None,
                options=['Home', 'User logs', 'Captured', 'About'],
                icons=['house-fill', 'person-circle', 'trophy-fill', 'info-circle-fill'],
                default_index=0,
                orientation="horizontal"
            )

            if app == "Home":
                Home.app()
            elif app == "User logs":
                User_logs.app()
            elif app == "Captured":
                Images_Captured.app()
            elif app == 'About':
                About.app()

    # Create an instance of the MultiApp class and run it
    multi_app = MultiApp()
    multi_app.run()
