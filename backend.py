"""Simple Task Manager backend built with FastAPI.

Stores tasks in memory (a plain Python list) so no database setup is needed.
Run with:  uvicorn backend:app --reload --port 8000
"""

from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Task Manager API", version="1.0.0")

# Allow the Streamlit frontend (served on a different port) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend's origin.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Task(BaseModel):
    """A single task."""

    id: int
    title: str
    done: bool = False


class TaskCreate(BaseModel):
    """Payload for creating a new task."""

    title: str = Field(..., min_length=1, description="The task description")


# In-memory storage. Seeded with one example task.
tasks: List[Task] = [
    Task(id=1, title="Learn FastAPI", done=False),
    Task(id=2, title="Build a Streamlit UI", done=True),
]
_next_id = 3


@app.get("/tasks", response_model=List[Task])
def list_tasks() -> List[Task]:
    """Return all tasks."""
    return tasks


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate) -> Task:
    """Add a new task and return it."""
    global _next_id
    task = Task(id=_next_id, title=payload.title.strip(), done=False)
    tasks.append(task)
    _next_id += 1
    return task


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    """Return a single task by id."""
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
