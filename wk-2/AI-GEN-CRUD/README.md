# AI-GEN CRUD Comparison

This folder contains an AI-generated version of your task API in [ai_gen.py](./ai_gen.py), meant to be compared with your handcoded version in [../main.py](../main.py).

## Run the AI version

From the `wk-2/AI-GEN-CRUD` folder:

```bash
uvicorn ai_gen:app --reload
```

## Diff command (AI vs your code)

From the `wk-2` folder:

```bash
git diff --no-index .\main.py .\AI-GEN-CRUD\ai_gen.py
```

If you prefer from repo root:

```bash
git diff --no-index .\wk-2\main.py .\wk-2\AI-GEN-CRUD\ai_gen.py
```

## AI vs me

### 1) What did the AI do better — and do I understand it well enough to explain?

- It extracted repeated lookup logic into `get_task_or_404`, which removes duplication in `GET /tasks/{id}` and `PUT /tasks/{id}`.
- It normalizes titles with `strip()` before storing them, so accidental leading/trailing spaces are cleaned.
- Yes, I understand this version well enough to explain each endpoint and helper.

### 2) What did it get wrong or quietly ignore from my prompt?

- Nothing major was ignored for this prompt: CRUD routes, health check, filtered list, update, delete, and stats are all present.
- It also includes `/reset`, which was an extra convenience endpoint (not strictly required in your latest prompt, but useful for demos).

### 3) What did my prompt forget to specify — and what did the AI silently decide?

- The prompt did not define exact response shape for errors, so the AI used FastAPI defaults (`detail` fields).
- The prompt did not define search behavior, so the AI chose case-insensitive substring matching on `title`.
- The prompt did not define persistence, so the AI kept in-memory storage only (same as your version).
