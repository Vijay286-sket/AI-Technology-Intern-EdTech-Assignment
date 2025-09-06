import os
import time
import random
from datetime import datetime
from typing import List, Dict

import streamlit as st
from dotenv import load_dotenv

# -----------------------------
# App Config
# -----------------------------
st.set_page_config(page_title="Iron Lady - MVP Suite", page_icon="💬", layout="centered")
load_dotenv()  # Load .env with GEMINI_API_KEY

# -----------------------------
# Utilities
# -----------------------------
FAQS = {
    "What is Iron Lady?": "Iron Lady is a leadership development platform focused on empowering women with practical leadership skills, confidence, and career acceleration.",
    "What programs do you offer?": "We offer leadership bootcamps, executive coaching, confidence-building workshops, and cohort-based programs tailored for different career stages.",
    "Who can join?": "Professionals, aspiring leaders, and women returning to the workforce—anyone looking to build leadership capabilities is welcome.",
    "How long are the programs?": "Programs range from short 2-hour workshops to 8–12 week cohort-based courses.",
    "Do you provide certificates?": "Yes, participants receive a certificate of completion for eligible programs.",
    "Is there a community?": "Yes, we provide an active peer community, mentorship, and alumni network for continued growth.",
}

SIMILARITY_KEYS = [k.lower() for k in FAQS.keys()]


def simple_match(query: str) -> str:
    """Minimal keyword-based matcher against known FAQs."""
    q = (query or "").strip().lower()
    if not q:
        return "Please ask a question about Iron Lady's leadership programs."

    # Exact match
    if q in FAQS:
        return FAQS[q]

    # Fuzzy contains match
    for key in SIMILARITY_KEYS:
        if key in q or q in key:
            return FAQS[[k for k in FAQS.keys() if k.lower() == key][0]]

    # Keyword hints
    hints = [
        ("program", "We offer leadership bootcamps, executive coaching, and workshops."),
        ("certificate", "Yes, certificates are provided for eligible programs."),
        ("duration", "Programs range from 2 hours to 8–12 weeks."),
        ("community", "Yes, we provide an active community, mentorship, and alumni network."),
        ("join", "Professionals and aspiring leaders can join; see our cohorts and workshops."),
    ]
    for word, ans in hints:
        if word in q:
            return ans

    return "I don't have that in my FAQs. Toggle 'Use AI if available' to try an AI answer or ask another question."


def ai_answer(query: str, api_key: str) -> str:
    """Try answering with Gemini if key available; otherwise return empty string.
    This is optional. The app works without it.
    """
    if not api_key:
        return ""
    try:
        import google.generativeai as genai  # lazy import
        genai.configure(api_key=api_key)
        prompt = (
            "You are a helpful assistant answering FAQs about a women's leadership program "
            "called Iron Lady. Be concise and factual. If unsure, say you are unsure.\n\n"
            f"User question: {query}"
        )
        model = genai.GenerativeModel("gemini-1.5-flash")
        resp = model.generate_content(prompt)
        return (resp.text or "").strip()
    except Exception:
        # Silently fail to keep UX simple
        return ""


def ai_short_task(api_key: str) -> str:
    """Generate one short, practical task using Gemini."""
    if not api_key:
        return ""
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        prompt = (
            "Suggest one short, practical task to improve leadership or productivity. "
            "Return only the task phrase."
        )
        model = genai.GenerativeModel("gemini-1.5-flash")
        resp = model.generate_content(prompt)
        return (resp.text or "").strip()
    except Exception:
        return ""


# -----------------------------
# Session State Setup
# -----------------------------
if "chat" not in st.session_state:
    st.session_state.chat: List[Dict] = []

if "tasks" not in st.session_state:
    st.session_state.tasks: List[Dict] = []


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("Iron Lady - MVP")
page = st.sidebar.radio("Go to", ["FAQ Chatbot", "To-Do Manager"], index=0)

st.sidebar.markdown("---")
use_ai = st.sidebar.checkbox("Use AI if available (Gemini)", value=False)
# Always load from .env
user_api_key = os.getenv("GEMINI_API_KEY", "")
if use_ai:
    if user_api_key:
        st.sidebar.success("GEMINI_API_KEY loaded from .env")
    else:
        st.sidebar.warning("No GEMINI_API_KEY found in .env")


# -----------------------------
# Pages
# -----------------------------
if page == "FAQ Chatbot":
    st.title("Iron Lady FAQ Chatbot 💬")
    st.caption("MVP: Hardcoded answers with optional AI fallback")

    # Display chat history
    for msg in st.session_state.chat:
        if msg["role"] == "user":
            st.chat_message("user").markdown(msg["content"])
        else:
            st.chat_message("assistant").markdown(msg["content"])

    # Input
    prompt = st.chat_input("Ask about Iron Lady's leadership programs...")

    if prompt:
        st.session_state.chat.append({"role": "user", "content": prompt})

        # First try simple matcher
        answer = simple_match(prompt)
        used_ai = False

        # Optional AI if requested and matcher responded with fallback
        if use_ai and ("I don't have that" in answer or "unsure" in answer.lower()):
            ai_resp = ai_answer(prompt, user_api_key)
            if ai_resp:
                answer = ai_resp
                used_ai = True

        # Show response
        tag = "(AI) " if used_ai else ""
        st.session_state.chat.append({"role": "assistant", "content": f"{tag}{answer}"})
        st.chat_message("assistant").markdown(f"{tag}{answer}")

    # Clear button
    if st.button("Clear chat"):
        st.session_state.chat = []
        st.success("Chat cleared.")

elif page == "To-Do Manager":
    st.title("Simple To-Do Manager ✅")
    st.caption("MVP: Create, view, complete, and delete tasks. Bonus: suggest a task (AI optional).")

    # Add task
    with st.form("add_task", clear_on_submit=True):
        title = st.text_input("New task", placeholder="e.g., Research upcoming cohort dates")
        submitted = st.form_submit_button("Add task")
        if submitted and title.strip():
            st.session_state.tasks.append({
                "id": f"t{int(time.time() * 1000)}",
                "title": title.strip(),
                "done": False,
                "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })
            st.toast("Task added", icon="✅")

    # Suggest task (Bonus AI)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Suggest a task (local)"):
            ideas = [
                "Draft a LinkedIn post about leadership learnings",
                "Block time for skill-building this week",
                "List 3 goals for the next cohort",
                "Prepare questions for a mentor call",
                "Summarize notes from last workshop",
            ]
            st.session_state.tasks.append({
                "id": f"t{int(time.time() * 1000)}",
                "title": random.choice(ideas),
                "done": False,
                "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })
            st.toast("Suggested task added", icon="✨")

    with col2:
        if st.button("Suggest a task (AI)"):
            suggestion = ""
            if use_ai and user_api_key:
                suggestion = ai_short_task(user_api_key)
            if suggestion:
                st.session_state.tasks.append({
                    "id": f"t{int(time.time() * 1000)}",
                    "title": suggestion,
                    "done": False,
                    "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                })
                st.toast("AI suggestion added", icon="🤖")
            else:
                st.info("AI not available or failed. Use 'Suggest a task (local)' instead.")

    st.markdown("---")
    st.subheader("Your Tasks")

    if not st.session_state.tasks:
        st.info("No tasks yet. Add one above.")
    else:
        # Display tasks with simple CRUD controls
        for idx, task in enumerate(list(st.session_state.tasks)):
            c1, c2, c3, c4 = st.columns([0.1, 0.7, 0.1, 0.1])
            with c1:
                done = st.checkbox("", value=task["done"], key=f"done_{task['id']}")
                task["done"] = done
            with c2:
                style = "text-decoration: line-through; color: gray;" if task["done"] else ""
                st.markdown(f"<div style='{style}'>{task['title']}</div>", unsafe_allow_html=True)
                st.caption(f"Created: {task['created']}")
            with c3:
                if st.button("Edit", key=f"edit_{task['id']}"):
                    new_title = st.text_input("Edit task", value=task["title"], key=f"title_{task['id']}")
                    if st.button("Save", key=f"save_{task['id']}"):
                        if new_title.strip():
                            task["title"] = new_title.strip()
                            st.success("Task updated")
                            st.experimental_rerun()
            with c4:
                if st.button("Delete", key=f"del_{task['id']}"):
                    st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task["id"]]
                    st.toast("Task deleted", icon="🗑️")
                    st.experimental_rerun()

    # Minimal summary helper for all completed tasks (local)
    st.markdown("---")
    if st.button("Summarize completed tasks"):
        completed = [t["title"] for t in st.session_state.tasks if t["done"]]
        if not completed:
            st.info("No completed tasks yet.")
        else:
            bullet = "\n".join([f"• {t}" for t in completed])
            st.success(f"You completed {len(completed)} task(s):\n{bullet}")

# End of app
