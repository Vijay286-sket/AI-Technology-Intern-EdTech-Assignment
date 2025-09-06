import os
import streamlit as st
from dotenv import load_dotenv

from src.pages.faq_chatbot import render as render_faq
from src.pages.todo_manager import render as render_todo


# -----------------------------
# App Config
# -----------------------------
st.set_page_config(page_title="Iron Lady - MVP Suite", page_icon="💬", layout="centered")
load_dotenv()  # Load .env with GEMINI_API_KEY


# -----------------------------
# Sidebar & Routing
# -----------------------------
st.sidebar.title("Iron Lady - MVP")
page = st.sidebar.radio("Go to", ["FAQ Chatbot", "To-Do Manager"], index=0)

st.sidebar.markdown("---")
use_ai = st.sidebar.checkbox("Use AI if available (Gemini)", value=False)
user_api_key = os.getenv("GEMINI_API_KEY", "")
if use_ai:
    if user_api_key:
        st.sidebar.success("GEMINI_API_KEY loaded from .env")
    else:
        st.sidebar.warning("No GEMINI_API_KEY found in .env")


# -----------------------------
# Page Dispatcher
# -----------------------------
if page == "FAQ Chatbot":
    render_faq(use_ai, user_api_key)
elif page == "To-Do Manager":
    render_todo(use_ai, user_api_key)

# End of app
