# Task Tracker Architecture — Strategy A

This document uses a minimal evidence set: `README.md` and the core application
files involved in task creation.

## 1. What it does

Task Tracker is a small full-stack task-management application. A vanilla
HTML/CSS/JavaScript Kanban board communicates with a FastAPI backend that
supports health checking and task create, read, update, and delete operations.
Tasks can be searched and filtered by status, priority, text, and overdue state.

The frontend and backend are served separately during local development:
the static frontend on port 5500 and Uvicorn on port 8000. The backend stores
tasks in a process-local Python dictionary, so data is not durable and is lost
when the process restarts.

Evidence: `README.md`, `app/main.py`, `app/storage.py`, and
`app/frontend/index.html`.

## 2. Data model

| Type | Fields and behavior |
| --- | --- |
| `TaskStatus` | `ToDo`, `InProgress`, or `Done`. |
| `TaskPriority` | `Low`, `Medium`, or `High`. |
| `TaskCreate` | Requires `title`; defaults `description` to `""`, `status` to `ToDo`, and `priority` to `Medium`; `assignee` and `due_date` are nullable. Extra fields are forbidden. Titles are trimmed, must not be empty, and may contain at most 200 characters. |
| `TaskUpdate` | Provides optional versions of the task input fields for partial updates. Extra fields are forbidden. A supplied title cannot be null or blank and is subject to the same 200-character limit. |
| `TaskResponse` | Contains the task fields plus a generated UUID string `id` and UTC `created_at` and `updated_at` timestamps. |

Stored tasks are `TaskResponse` objects held in
`dict[str, TaskResponse]`, keyed by task ID. A task is overdue when it has a
due date before today and its status is not `Done`.

Evidence: `app/models.py` and `app/storage.py`.

## 3. Request flow when a user creates a task

1. The user submits the task modal in `app/frontend/index.html`.
2. The frontend trims the title and sends `POST /tasks` with JSON containing
   `title`, `description`, `status`, `priority`, `assignee`, and `due_date`.
3. FastAPI parses the body as `TaskCreate`; Pydantic applies defaults, rejects
   extra fields, and validates and normalizes the title.
4. The `create_task` route delegates the validated payload to
   `storage.add_task`.
5. Storage constructs a `TaskResponse`, which generates the ID and timestamps,
   then inserts it into the in-memory dictionary.
6. FastAPI serializes the stored task and returns it with HTTP 201.
7. On success, the frontend closes the modal and refreshes the board with
   `GET /tasks`. Validation or request failures remain visible in the modal.

In compact form:

`Browser form → POST /tasks → TaskCreate validation → create_task() → storage.add_task() → in-memory dictionary → HTTP 201 → board refresh`

Evidence: `app/frontend/index.html`, `app/main.py`, `app/models.py`, and
`app/storage.py`.

## 4. Key files

| File | Responsibility |
| --- | --- |
| `app/main.py` | FastAPI application, CORS configuration, health endpoint, task routes, response models, and HTTP status handling. |
| `app/models.py` | Pydantic request/response models, enums, defaults, generated fields, and title validation. |
| `app/storage.py` | In-memory persistence plus task creation, retrieval, filtering, partial update, deletion, and overdue calculation. |
| `app/business_rules.py` | Allowed task-status transitions and transition validation. |
| `app/frontend/index.html` | Self-contained Kanban UI, styling, browser state, form handling, and API calls. |
| `tests/test_tasks.py` | Main pytest file identified by the documented project structure. |
| `README.md` | Supported setup, run, test, architecture, and documentation guidance. |

## 5. Conventions

- Status and priority values use the exact casing defined by their enums.
- Allowed status transitions are `ToDo → InProgress`,
  `InProgress → Done`, and `Done → InProgress`; other requested transitions
  produce HTTP 422.
- Route handlers coordinate HTTP behavior, Pydantic models own request
  validation, storage owns in-memory data operations, and
  `business_rules.py` owns transition policy.
- Partial updates use `PATCH /tasks/{task_id}` and apply only explicitly
  supplied fields; successful updates refresh `updated_at`.
- Missing task IDs produce HTTP 404. Successful deletion produces HTTP 204
  with no response body.
- Public Python functions use Google-style docstrings. Private
  underscore-prefixed helpers are treated as internal implementation details.
- The frontend has no build step and is served separately from the API.

Evidence: `README.md`, `app/main.py`, `app/models.py`, `app/storage.py`, and
`app/business_rules.py`.
