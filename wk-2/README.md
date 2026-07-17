# Task API

Task API is a small FastAPI project that demonstrates the CRUD cycle with an in-memory list of tasks. It includes read, create, update, and delete endpoints, plus built-in Swagger UI at `/docs`.

## How to run

1. Activate your virtual environment.
2. Install the project dependencies if you have not already.
3. Start the server from the `wk-2` folder with:

```bash
uvicorn main:app --reload
```

Then open:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/docs`

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | `/` | Returns basic API info |
| GET | `/health` | Returns server health status |
| GET | `/tasks` | Returns all tasks |
| GET | `/tasks/{task_id}` | Returns one task by id |
| POST | `/tasks` | Creates a new task |
| PUT | `/tasks/{task_id}` | Updates an existing task |
| DELETE | `/tasks/{task_id}` | Deletes a task |

## Example request

Create a task:

```bash
curl -i -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Buy milk\"}"
```

Example response:

```http
HTTP/1.1 201 Created
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

## Swagger UI

Open `http://127.0.0.1:8000/docs` and use `Try it out` to test the full CRUD flow.

Add your Swagger screenshot here after you capture it:

![Swagger UI screenshot](swagger-screenshot.png)

## Notes

- The data lives only in memory, so restarting the server resets the task list.
- Validation returns `400` for empty titles and `404` when a task id does not exist.
- Swagger UI is built into FastAPI, so no extra setup is needed for `/docs`.