"""Simple Task Manager frontend built with Streamlit.

Talks to the FastAPI backend (backend.py). Make sure the backend is running
on http://localhost:8000 before starting this app.

Run with:  streamlit run app.py
"""

import requests
import streamlit as st

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Task Manager", page_icon="✅")
st.title("✅ Task Manager")
st.caption(f"Connected to backend at {BACKEND_URL}")


def fetch_tasks() -> list[dict]:
    """Fetch all tasks from the backend."""
    response = requests.get(f"{BACKEND_URL}/tasks", timeout=10)
    response.raise_for_status()
    return response.json()


def add_task(title: str) -> None:
    """Create a new task on the backend."""
    response = requests.post(
        f"{BACKEND_URL}/tasks", json={"title": title}, timeout=10
    )
    response.raise_for_status()


# --- Add a new task ---
with st.form("add_task_form", clear_on_submit=True):
    new_title = st.text_input("New task", placeholder="e.g. Buy groceries")
    submitted = st.form_submit_button("Add task")
    if submitted:
        if new_title.strip():
            try:
                add_task(new_title.strip())
                st.success(f"Added: {new_title.strip()}")
            except requests.RequestException as exc:
                st.error(f"Failed to add task: {exc}")
        else:
            st.warning("Please enter a task description.")

st.divider()

# --- Display the task list ---
st.subheader("Your tasks")
try:
    tasks = fetch_tasks()
    if not tasks:
        st.info("No tasks yet. Add one above!")
    else:
        for task in tasks:
            done = task.get("done", False)
            label = f"**#{task['id']}** — {task['title']}"
            checkbox = st.checkbox(label, value=done, key=f"task_{task['id']}")
            # Read-only display of completion state (backend has no toggle endpoint).
            if checkbox != done:
                st.toast("Toggle is display-only in this demo.", icon="ℹ️")
except requests.RequestException as exc:
    st.error(
        "Could not reach the backend. "
        "Is it running? Start it with: uvicorn backend:app --port 8000"
    )
    st.code(str(exc))
