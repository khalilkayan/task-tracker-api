# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 1. Tech stack

- Python 3.11
- FastAPI
- Pydantic v2
- Uvicorn
- pytest
- httpx
- Vanilla HTML/CSS/JavaScript frontend (`app/frontend/index.html`, no build step, no `package.json`)

## 2. Exact commands

Setup:

```bash
python3.11 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

Backend (terminal 1):

```bash
uvicorn app.main:app --reload --port 8000
```

Frontend (terminal 2):

```bash
python3 -m http.server 5500 --directory app/frontend
```

Open http://localhost:5500 while the backend runs on port 8000.

Tests:

```bash
pytest -v
```

Standalone validation script (not collected by pytest — filename doesn't match `test_*.py`; run directly):

```bash
PYTHONPATH=. python tests/verify_a.py
```

No linter or formatter is configured in this repo.

## 3. Architecture

FastAPI backend + vanilla JS frontend, with **in-memory** storage (no database). State resets on process restart.

- `app/main.py` — all HTTP routes (`/health`, `/tasks` CRUD, `GET /tasks` with `status`/`priority`/`q`/`overdue` query params). Thin: delegates to `storage`, raises `HTTPException` on not-found, and defers status-transition validation to `business_rules`.
- `app/models.py` — Pydantic models and the two enums (`TaskStatus`, `TaskPriority`). `TaskCreate`/`TaskUpdate` use `extra="forbid"`. `TaskResponse` generates its own `id`/`created_at`/`updated_at` defaults.
- `app/storage.py` — the entire persistence layer: a single module-level `dict[str, TaskResponse]`. Owns query/filter logic (`get_all_tasks`) and the overdue rule (`_is_task_overdue`). `update_task` uses `payload.model_dump(exclude_unset=True)`, so an omitted field is left unchanged while an explicit `null` clears it (e.g. removing `due_date`). `_reset()` clears state.
- `app/business_rules.py` — status-transition validation only; `VALID_TRANSITIONS` is the single source of truth.
- `app/frontend/index.html` — self-contained Kanban board (inline CSS/JS, no framework). Talks to the API via `fetch` against `API_BASE = "http://localhost:8000"`. It reimplements the overdue check client-side (`isTaskOverdue()`) independently of `storage._is_task_overdue` — keep both in sync if the rule changes.
- `tests/conftest.py` — `client` fixture (`TestClient(app)`), `created_task` fixture, and an autouse `_reset_storage` fixture that calls `storage._reset()` before and after every test so no task state leaks between tests.
- `tests/test_tasks.py` — the pytest suite (28 tests as of the last verified run).
- `tests/verify_a.py` — a standalone script exercising `app.models`/`app.storage` directly; not picked up by `pytest` (filename doesn't match `test_*.py`).

## 4. Business rules

`TaskStatus` values: `ToDo`, `InProgress`, `Done`.

Legal transitions (`business_rules.VALID_TRANSITIONS`, exhaustive):

- `ToDo` → `InProgress`
- `InProgress` → `Done`
- `Done` → `InProgress`

Any other transition (e.g. `ToDo` → `Done` directly) returns `422` with an "Invalid status transition" message listing the allowed moves.

Overdue rule (`storage._is_task_overdue`): a task is overdue only if it has a `due_date`, that `due_date` is before today, and `status != Done`.

Combined filtering (`storage.get_all_tasks`): `q` (case-insensitive substring match on title or description), `status`, `priority`, and `overdue=true` are each optional and independently combinable via `GET /tasks` query params — all supplied filters apply together (AND).

## 5. UI and local development

- Backend runs on port 8000; the frontend's `API_BASE` is hardcoded to `http://localhost:8000`, so the backend must be started on that port.
- Frontend is served on port 5500 via `python3 -m http.server 5500 --directory app/frontend` (see section 2).
- CORS (`app/main.py`): `allow_origins = ["http://localhost:5500", "http://127.0.0.1:5500", "http://localhost:5173", "null"]`, `allow_credentials=False`, `allow_methods=["*"]`, `allow_headers=["*"]`.
- Board: three columns (ToDo/InProgress/Done), drag-and-drop to change status, New/Edit modal, search + priority + overdue-only filter toolbar, per-card "Overdue" pill.

## 6. Documentation

`docs/midcourse/` contains the ADR (`mini-adr.md`), user stories, prompt log, reflection, and verification notes for the two mid-course features (search/filters, due dates/overdue). Check `mini-adr.md` before making architectural changes — it lists what was deliberately rejected (pagination, datetime due dates, notifications, a separate search endpoint, frontend-only filtering/overdue calculation).

## 7. Do-not rules

- Do not add authentication.
- Do not add a database.
- Do not add deployment steps.
- Do not make unrelated UI changes.
- Do not change business rules without asking.
- Do not add dependencies without approval.
