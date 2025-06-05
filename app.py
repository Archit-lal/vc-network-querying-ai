import streamlit as st
from src.ui import main_ui

st.set_page_config(
    page_title="SpringBank Network", 
    page_icon="💰",
    layout="wide",
)

main_ui()