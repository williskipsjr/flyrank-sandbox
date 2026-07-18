from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


# FastAPI app for the task API.
app = FastAPI()


def seed_tasks() -> list[dict]:
    # Starter data used on first boot and whenever /reset is called.
    return [
        {"id": 1, "title": "Buy milk", "done": False},
        {"id": 2, "title": "Walk the dog", "done": True},
        {"id": 3, "title": "Read FastAPI docs", "done": False},
    ]

tasks = seed_tasks()


class TaskCreate(BaseModel):
    # Request body for creating a task.
    title: str


class TaskUpdate(BaseModel):
    # Request body for updating a task.
    title: str | None = None
    done: bool | None = None


def next_task_id() -> int:
    # Find the next available task id.
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


@app.get("/", summary="API info")
def root():
    # Return basic API details.
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks", "/stats", "/reset"],
    }


@app.get("/health", summary="Health check")
def health():
    # Simple server health check.
    return {"status": "ok"}

@app.get("/tasks", summary="List tasks (with optional filtering/search)")
def get_tasks(done: bool | None = None, search: str | None = None):
    # Start from the full list, then apply optional filters.
    filtered = tasks

    # done=true or done=false returns only matching completion state.
    if done is not None:
        filtered = [task for task in filtered if task["done"] == done]

    # search=milk performs a case-insensitive title match.
    if search is not None and search.strip():
        term = search.strip().lower()
        filtered = [task for task in filtered if term in task["title"].lower()]
    return filtered


@app.get("/tasks/{task_id}", summary="Get one task")
def get_task(task_id: int):
    # Find one task by id.
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.post("/tasks", status_code=status.HTTP_201_CREATED, summary="Create a task")
def create_task(payload: TaskCreate):
    # Reject empty titles before saving.
    if not payload.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")

    # Build the new task and store it in memory.
    task = {
        "id": next_task_id(),
        "title": payload.title,
        "done": False,
    }
    tasks.append(task)
    return task


@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, payload: TaskUpdate):
    # Update the task when the id exists.
    for task in tasks:
        if task["id"] == task_id:
            if payload.title is not None:
                if not payload.title.strip():
                    raise HTTPException(status_code=400, detail="Title must not be empty")
                task["title"] = payload.title
            if payload.done is not None:
                task["done"] = payload.done
            return task

    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a task")
def delete_task(task_id: int):
    # Remove the task when the id exists.
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return None

    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.get("/stats", summary="Task stats")
def get_stats():
    # Compute aggregate values from the current in-memory task list.
    total = len(tasks)
    done = sum(1 for task in tasks if task["done"])
    open_tasks = total - done
    return {"total": total, "done": done, "open": open_tasks}

@app.post("/reset", summary="Reset tasks to the starter set")
def reset_tasks():
    # Reset the task list to the original seed tasks.
    tasks.clear()
    tasks.extend(seed_tasks())
    return {"message": "Tasks reset to starter data", "total": len(tasks)}




