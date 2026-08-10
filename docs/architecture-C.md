# Task Tracker Architecture — Strategy C

This document is based only on `app/main.py`, `app/models.py`, and
`app/storage.py`.

## 1. What it does

The application is a FastAPI service for managing tasks. It provides:

- A health endpoint returning service status and a UTC timestamp.
- Task creation, listing, retrieval, partial update, and deletion.
- List filtering by status, priority, case-insensitive text search, and
  overdue state.
- CORS access for the configured local frontend origins.

Tasks are held in process memory. Persistence across process restarts,
authentication, deployment topology, and client behavior are not visible
from the files I read.

## 2. Data model

`TaskCreate` accepts a required title and optional description, status,
priority, assignee, and due date. Status defaults to `ToDo`, priority
defaults to `Medium`, and extra fields are forbidden.

`TaskUpdate` exposes the same editable fields as optional values for partial
updates and also forbids extra fields. A supplied title is stripped and must
contain between 1 and 200 characters.

`TaskResponse` adds a UUID string identifier plus UTC `created_at` and
`updated_at` timestamps. Status values are `ToDo`, `InProgress`, and `Done`;
priority values are `Low`, `Medium`, and `High`.

## 3. Request flow when a user creates a task

1. A client sends `POST /tasks` with a JSON request body.
2. FastAPI and Pydantic parse the body as `TaskCreate`, reject extra fields,
   validate the enums, and normalize and validate the title.
3. `create_task` passes the validated model to `storage.add_task`.
4. Storage converts the creation model into `TaskResponse`. Model defaults
   generate the UUID and UTC timestamps.
5. Storage inserts the task into the module-level `_tasks` dictionary,
   keyed by task ID.
6. The API serializes the stored task through the `TaskResponse` response
   model and returns HTTP 201.

## 4. Key files

- `app/main.py`: Creates the FastAPI application, configures CORS, declares
  the health and task routes, delegates persistence operations to storage,
  and maps missing tasks to HTTP 404 responses. It imports status-transition
  validation, but that implementation is not visible from the files I read.
- `app/models.py`: Defines task status and priority enums plus the creation,
  update, and response schemas and title validation.
- `app/storage.py`: Implements the in-memory task dictionary and task CRUD,
  filtering, overdue detection, and storage reset behavior.

## 5. Conventions

- Route handlers and storage functions are synchronous and type-annotated.
- API input and output are represented by Pydantic models.
- Creation and update payloads reject undeclared fields.
- IDs are UUID strings, timestamps use UTC, and due dates are date-only.
- Partial updates apply only explicitly supplied fields and refresh
  `updated_at`.
- Search is trimmed and case-insensitive; supplied filters use AND semantics.
- A task is overdue when its due date is earlier than today and its status is
  not `Done`.
- Missing individual tasks produce HTTP 404; successful deletion produces
  HTTP 204 without a response body.
