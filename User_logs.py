import streamlit as st
import pandas as pd
import os

def app():
    st.title("User Log - Detection Logs")
    csv_file = "output/Recordings.csv"

    if st.button("Refresh"):
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file, names=["Name", "Detection Time"])
            st.dataframe(df)
        else:
            st.warning("No detection log found.")
    else:
        st.warning("Click 'Refresh' to load detection log.")
