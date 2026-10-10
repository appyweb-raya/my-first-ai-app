# ✅ Task Manager

A simple full-stack Task Manager built to learn the AI-assisted development
workflow. It uses **FastAPI** for the backend API and **Streamlit** for the
frontend, with tasks stored in memory.

## Project structure

| File | Purpose |
|------|---------|
| `backend.py` | FastAPI app exposing `GET /tasks` and `POST /tasks` |
| `app.py` | Streamlit UI that lists tasks and lets you add new ones |
| `test_app.py` | Headless smoke test for the Streamlit app (uses Streamlit's `AppTest`) |
| `requirements.txt` | Pinned Python dependencies |

## Prerequisites

- Python 3.10+ (developed and tested on 3.14)

## Setup

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Run the app

You need **two terminals** — one for the backend and one for the frontend.

**Terminal 1 — backend (FastAPI):**

```bash
uvicorn backend:app --reload --port 8000
```

**Terminal 2 — frontend (Streamlit):**

```bash
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

## API reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/tasks` | List all tasks |
| `POST` | `/tasks` | Add a task. Body: `{"title": "..."}` |
| `GET`  | `/tasks/{id}` | Fetch a single task by id |

Interactive API docs are available at http://localhost:8000/docs while the
backend is running.

## Testing

With the backend running, execute the headless frontend smoke test:

```bash
python test_app.py
```

It verifies the app renders the task list and that adding a task increases the
total. A passing run prints `TEST_RESULT PASS`.
