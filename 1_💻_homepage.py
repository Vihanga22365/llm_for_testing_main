import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from dotenv import load_dotenv
import os


st.set_page_config(
    page_title="Test Case Generator",
    page_icon="🖥️",
    initial_sidebar_state="collapsed"
    
)

st.title("Test Case Generator")


col1,col2=st.columns(2)

with col1:
    if st.button('API Tests'):
        switch_page("API Tests")

with col2:
    if st.button('User Interface Tests'):
        switch_page("User Interface tests")


