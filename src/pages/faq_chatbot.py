from typing import List, Dict
import streamlit as st

from src.data.faqs import simple_match
from src.utils.ai import ai_answer


def render(use_ai: bool, api_key: str):
    st.title("Iron Lady FAQ Chatbot 💬")
    st.caption("MVP: Hardcoded answers with optional AI fallback")

    if "chat" not in st.session_state:
        st.session_state.chat: List[Dict] = []

    # Show history
    for msg in st.session_state.chat:
        if msg["role"] == "user":
            st.chat_message("user").markdown(msg["content"])
        else:
            st.chat_message("assistant").markdown(msg["content"])

    prompt = st.chat_input("Ask about Iron Lady's leadership programs...")

    if prompt:
        st.session_state.chat.append({"role": "user", "content": prompt})
        answer = simple_match(prompt)
        used_ai = False

        if use_ai and ("I don't have that" in answer or "unsure" in answer.lower()):
            ai_resp = ai_answer(prompt, api_key)
            if ai_resp:
                answer = ai_resp
                used_ai = True

        tag = "(AI) " if used_ai else ""
        st.session_state.chat.append({"role": "assistant", "content": f"{tag}{answer}"})
        st.chat_message("assistant").markdown(f"{tag}{answer}")

    if st.button("Clear chat"):
        st.session_state.chat = []
        st.success("Chat cleared.")
