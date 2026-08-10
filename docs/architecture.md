# Task Tracker Architecture

## 1. What it does

Task Tracker is a small task-management system with a FastAPI backend and a
no-build vanilla HTML, CSS, and JavaScript frontend. The browser presents a
task board, while the API provides health checking and task creation, listing,
retrieval, partial update, and deletion.

Task lists can be filtered by status, priority, case-insensitive text search,
and overdue state. CORS is configured for local frontend access.

Tasks are stored in a process-local Python dictionary. The storage is
non-durable, so task data is lost when the application process restarts.

## 2. Data model

Task input and output are represented by Pydantic models using two string enums.

| Type | Fields and behavior |
| --- | --- |
| `TaskStatus` | `ToDo`, `InProgress`, or `Done`. |
| `TaskPriority` | `Low`, `Medium`, or `High`. |
| `TaskCreate` | Requires `title`; defaults `description` to `""`, `status` to `ToDo`, and `priority` to `Medium`; `assignee` and `due_date` are nullable. Extra fields are forbidden. |
| `TaskUpdate` | Provides optional editable fields for partial updates and forbids extra fields. A supplied title cannot be null or blank. |
| `TaskResponse` | Contains the task fields plus a generated UUID string `id` and UTC `created_at` and `updated_at` timestamps. |

Titles are trimmed and must contain between 1 and 200 characters. Due dates
are date-only values. Stored `TaskResponse` objects are keyed by task ID in the
in-memory dictionary.

A task is overdue when its due date is earlier than today and its status is not
`Done`.

## 3. Request flow when a user creates a task

1. The user submits task details from the browser interface.
2. Browser JavaScript trims and checks the title, then sends a JSON body to
   `POST /tasks`.
3. FastAPI parses the body as `TaskCreate`; Pydantic validates the fields,
   applies defaults, rejects extra fields, and normalizes the title.
4. The `create_task` route passes the validated model to `storage.add_task`.
5. Storage constructs a `TaskResponse`, generating its ID and timestamps, and
   inserts it into the in-memory task dictionary.
6. FastAPI serializes the stored task and returns HTTP 201.
7. The frontend closes the creation modal and reloads the task list with
   `GET /tasks` so the board can be rendered with current data.

In compact form:

`Browser form → POST /tasks → TaskCreate validation → route handler → storage.add_task() → in-memory dictionary → HTTP 201 → board refresh`

## 4. Key files

| File | Responsibility |
| --- | --- |
| `app/main.py` | Creates the FastAPI application, configures CORS, declares health and task routes, delegates data operations to storage, and maps API outcomes to HTTP responses. |
| `app/models.py` | Defines status and priority enums, request and response schemas, defaults, generated fields, and title validation. |
| `app/storage.py` | Implements the process-local task dictionary, CRUD operations, filtering, overdue detection, and timestamp updates. |
| `app/business_rules.py` | Defines and validates permitted task-status transitions. |
| `app/frontend/index.html` | Contains the no-build browser interface, styling, form behavior, board state, and API calls. |

## 5. Conventions and behavior

- Status and priority values use the exact casing defined by their enums.
- Allowed status transitions are `ToDo` → `InProgress`, `InProgress` → `Done`,
  and `Done` → `InProgress`.
- Route handlers coordinate HTTP behavior, Pydantic models own request
  validation, storage owns in-memory data operations, and the business-rules
  module owns transition policy.
- Partial updates use `PATCH /tasks/{task_id}`, apply only explicitly supplied
  fields, and refresh `updated_at`.
- Supplied list filters use AND semantics. Search text is trimmed and matched
  case-insensitively.
- Missing task IDs return HTTP 404, invalid status transitions return HTTP 422,
  and successful deletion returns HTTP 204 without a response body.

## Context Strategy Comparison

### Strategy A - Minimal Context
What it got right: Strategy A produced a clear end-to-end architecture overview and correctly connected the frontend, API validation, storage layer, response flow, and board refresh.
What it got wrong or invented: Strategy A was less disciplined about its context boundaries and made some broader repository claims without clearly separating what it had directly verified from what it inferred.

### Strategy B - Structured Context
What it got right: Strategy B gave the most balanced repository-wide view because the structured context helped it connect the backend, frontend, storage, business rules, and project conventions without becoming too narrow.
What it got wrong or missed: Strategy B was broader and more useful than the other drafts, but it was less explicit about which details came directly from repository evidence and which came from the structured context it was given.

### Strategy C - Targeted Context
What it got right: Strategy C had the clearest evidence boundary because it stayed within the three approved files and explicitly said when information was not visible instead of filling gaps with assumptions.
What it got wrong or missed: Strategy C was intentionally too narrow for a full architecture overview because it could not describe the frontend, business-rule implementation, tests, or broader repository conventions from only three backend files.

### Verdict
I picked Strategy B because it gave the best balance between repository-wide coverage and useful structure, while still staying grounded enough to produce an architecture document I could realistically hand to someone else.

### My context rule
For repository-wide architecture or planning tasks, I use structured context because it gives enough breadth to connect the important files and conventions without relying on a completely open-ended search.
For focused implementation or review tasks with a known set of relevant files, I use targeted context because it keeps the evidence boundary clear and reduces the chance of unsupported assumptions.