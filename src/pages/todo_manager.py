import time
import random
from datetime import datetime
from typing import List, Dict

import streamlit as st

from src.utils.ai import ai_short_task


def render(use_ai: bool, api_key: str):
    st.title("Simple To-Do Manager ✅")
    st.caption("MVP: Create, view, complete, and delete tasks. Bonus: suggest a task (AI optional).")

    if "tasks" not in st.session_state:
        st.session_state.tasks: List[Dict] = []

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
            if use_ai and api_key:
                suggestion = ai_short_task(api_key)
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

    st.markdown("---")
    if st.button("Summarize completed tasks"):
        completed = [t["title"] for t in st.session_state.tasks if t["done"]]
        if not completed:
            st.info("No completed tasks yet.")
        else:
            bullet = "\n".join([f"• {t}" for t in completed])
            st.success(f"You completed {len(completed)} task(s):\n{bullet}")
