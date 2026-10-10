"""Headless smoke test for app.py using Streamlit's AppTest framework.

This runs app.py's script logic against the live backend and asserts that:
  - it renders without raising,
  - it lists the seeded tasks,
  - the add-task flow posts a new task and refreshes the list.

Run with:  python test_app.py   (backend must be running on :8000)
"""

import sys


def _force_utf8() -> None:
    """Make stdout/stderr tolerate emoji on Windows consoles."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


import requests
from streamlit.testing.v1 import AppTest

BACKEND = "http://127.0.0.1:8000"


def main() -> int:
    _force_utf8()
    # Ensure the backend is reachable before testing the frontend.
    try:
        requests.get(f"{BACKEND}/tasks", timeout=10).raise_for_status()
    except requests.RequestException as exc:
        print("BACKEND_UNREACHABLE", exc)
        return 1

    at = AppTest.from_file("app.py", default_timeout=30).run()

    if at.exception:
        print("APP_EXCEPTION", repr(at.exception[0].value))
        return 1

    titles = [t.value for t in at.title] + [c.value for c in at.caption]
    print("TITLES_AND_CAPTIONS", titles)

    # Checkbox labels contain the task text (value is just the bool state).
    checkbox_labels = [str(c.label) for c in at.checkbox]
    print("CHECKBOX_LABELS", checkbox_labels)

    # The seeded "Learn FastAPI" task should be rendered somewhere in the app.
    has_seeded_task = any("Learn FastAPI" in lbl for lbl in checkbox_labels)
    print("HAS_SEEDED_TASK", has_seeded_task)

    # Simulate adding a task through the form, then confirm the list grows.
    before = len(requests.get(f"{BACKEND}/tasks", timeout=10).json())
    at.text_input[0].set_value("Task from AppTest")
    at = at.button[0].click().run()
    if at.exception:
        print("APP_EXCEPTION_ON_ADD", repr(at.exception[0].value))
        return 1
    after = len(requests.get(f"{BACKEND}/tasks", timeout=10).json())

    print("TASKS_BEFORE", before, "TASKS_AFTER", after)
    print("ADD_INCREASED_COUNT", after == before + 1)

    success = has_seeded_task and after == before + 1
    print("TEST_RESULT", "PASS" if success else "FAIL")
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
