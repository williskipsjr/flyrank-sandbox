from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


app = FastAPI(title="AI Generated Task API")


def seed_tasks() -> list[dict]:
    return [
        {"id": 1, "title": "Buy milk", "done": False},
        {"id": 2, "title": "Walk the dog", "done": True},
        {"id": 3, "title": "Read FastAPI docs", "done": False},
    ]


tasks = seed_tasks()


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


def next_task_id() -> int:
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


def get_task_or_404(task_id: int) -> dict:
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.get("/", summary="API info")
def root():
    return {
        "name": "AI Generated Task API",
        "version": "1.0",
        "endpoints": ["/tasks", "/health", "/stats", "/reset"],
    }


@app.get("/health", summary="Health check")
def health():
    return {"status": "ok"}


@app.get("/tasks", summary="List tasks with optional filters")
def list_tasks(done: bool | None = None, search: str | None = None):
    filtered = tasks

    if done is not None:
        filtered = [task for task in filtered if task["done"] == done]

    if search is not None and search.strip():
        term = search.strip().lower()
        filtered = [task for task in filtered if term in task["title"].lower()]

    return filtered


@app.get("/tasks/{task_id}", summary="Get one task")
def get_task(task_id: int):
    return get_task_or_404(task_id)


@app.post("/tasks", status_code=status.HTTP_201_CREATED, summary="Create a task")
def create_task(payload: TaskCreate):
    title = payload.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")

    task = {"id": next_task_id(), "title": title, "done": False}
    tasks.append(task)
    return task


@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, payload: TaskUpdate):
    task = get_task_or_404(task_id)

    if payload.title is not None:
        title = payload.title.strip()
        if not title:
            raise HTTPException(status_code=400, detail="Title must not be empty")
        task["title"] = title

    if payload.done is not None:
        task["done"] = payload.done

    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a task")
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return None
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.get("/stats", summary="Task stats")
def stats():
    total = len(tasks)
    done = sum(1 for task in tasks if task["done"])
    return {"total": total, "done": done, "open": total - done}


@app.post("/reset", summary="Reset to starter tasks")
def reset_tasks():
    tasks.clear()
    tasks.extend(seed_tasks())
    return {"message": "Tasks reset to starter data", "total": len(tasks)}