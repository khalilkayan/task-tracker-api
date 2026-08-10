# Task Tracker Architecture — Strategy B

## 1. What it does

The project is a small task-management system with a FastAPI backend and a no-build HTML, CSS, and JavaScript task board. Users can create, view, filter, edit, move, and delete tasks through the API; the browser interface supports creation, editing, filtering, and drag-and-drop status changes.

The API also exposes a health endpoint. Task data is held only in server memory, so it is cleared whenever the application process restarts.

## 2. Data model

Task data is defined with Pydantic models and two string enums:

| Field | Type and behavior |
| --- | --- |
| `title` | Required string; whitespace is stripped; must contain 1–200 characters |
| `description` | Optional string; defaults to an empty string on creation |
| `status` | `ToDo`, `InProgress`, or `Done`; defaults to `ToDo` |
| `priority` | `Low`, `Medium`, or `High`; defaults to `Medium` |
| `assignee` | Optional string |
| `due_date` | Optional date |

`TaskCreate` defines creation input and rejects undeclared fields.

`TaskUpdate` makes fields optional for partial updates and also rejects undeclared fields. If `title` is supplied, it must be non-null and satisfy the creation title rules.

`TaskResponse` adds a UUID4 string identifier plus UTC `created_at` and `updated_at` timestamps.

## 3. Request flow when a user creates a task

1. The user opens the frontend modal, enters task details, and submits the form.
2. Browser JavaScript trims and checks the title, then sends JSON in `POST /tasks`.
3. FastAPI parses the body as `TaskCreate`; Pydantic validates fields, applies defaults for omitted values, and rejects invalid input before the route runs.
4. `create_task` delegates to `storage.add_task`.
5. Storage constructs a `TaskResponse`, generating its ID and timestamps, and inserts it into the process-local `_tasks` dictionary keyed by ID.
6. FastAPI returns the task as JSON with HTTP 201. The frontend closes the modal, reloads the current task list with `GET /tasks`, and renders the board.

## 4. Key files

| File | Role |
| --- | --- |
| `app/main.py` | Creates the FastAPI app, configures CORS, and defines health and task CRUD routes |
| `app/models.py` | Defines enums, request and response schemas, defaults, and title validation |
| `app/storage.py` | Implements in-memory CRUD operations, filtering, and overdue detection |
| `app/business_rules.py` | Defines and validates permitted status transitions |
| `app/frontend/index.html` | Contains the complete browser UI, styling, state handling, and API client |
| `app/__init__.py` | Marks `app` as an importable Python package |

## 5. Conventions

- Status values are exactly `ToDo`, `InProgress`, and `Done`; priority values are exactly `Low`, `Medium`, and `High`.
- Allowed status changes are `ToDo` → `InProgress`, `InProgress` → `Done`, and `Done` → `InProgress`.
- Request schemas reject extra fields, and task updates use partial `PATCH` semantics.
- Missing task IDs return HTTP 404; schema failures and invalid status transitions return HTTP 422.
- List filters use AND semantics; blank search text and `overdue=false` do not add filters.
- Storage is process-local and non-durable; identifiers use UUID4 strings and timestamps use UTC.
