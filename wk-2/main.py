## Stage 0, 1 and 2 of the CRUD API project.


from fastapi import FastAPI, HTTPException

app = FastAPI()


tasks = [
    {"id": 1, "title": "Buy Milk", "done": False},
    {"id": 2, "title": "Walk the dog", "done": True},
    {"id": 3, "title": "Read FastAPI docs", "done": False},
]

@app.get("/")
def root():
    return {"name": "Task API",
            "version": "1.0",
            "endpoints": ["/tasks"]
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


## Stage 3 : Create endpoints with validation and error handling

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, field_validator

class Task(BaseModel):
    title: str

    @field_validator('title')
    @classmethod
    def title_must_not_be_empty(cls, value: str):
        if not value.strip():
            raise ValueError("Title must not be empty")
        return value
    

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


def next_task_id():
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1