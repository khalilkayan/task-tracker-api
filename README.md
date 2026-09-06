# Task Tracker API

[![CI](https://github.com/khalilkayan/task-tracker-api/actions/workflows/ci.yml/badge.svg)](https://github.com/khalilkayan/task-tracker-api/actions/workflows/ci.yml)

A full-stack task-management application with a FastAPI/Pydantic REST API and a responsive vanilla JavaScript Kanban board.

## Overview

The backend exposes a focused, well-validated REST API for tasks: creation, retrieval,
partial updates, deletion, and combined query filtering. The frontend is a
self-contained Kanban board that consumes that API directly in the browser, with no
build step and no framework.

Developed and verified as the final project for the American University of Beirut (AUB)
AI-Assisted Coding Professional Certificate.

## Features

- Task creation, retrieval, partial updates, and deletion
- `ToDo`, `InProgress`, and `Done` Kanban columns
- Drag-and-drop status changes
- Validated workflow transitions: `ToDo` → `InProgress` → `Done`, with `Done` → `InProgress` for reopening
- Low, Medium, and High priorities
- Optional descriptions, assignees, and due dates
- Search across task titles and descriptions
- Status, priority, and overdue filters
- Search and filters combine with AND semantics
- Overdue indicators for unfinished tasks past their due date
- Responsive vanilla JavaScript interface

## Technology

- Python 3.11
- FastAPI
- Pydantic v2
- Uvicorn
- pytest
- HTML, CSS, and vanilla JavaScript
- Docker
- GitHub Actions

## Architecture

- FastAPI backend
- Pydantic v2 request and response models
- Business rules separated into `app/business_rules.py`
- In-memory dictionary storage in `app/storage.py`
- State resets whenever the backend process restarts
- Self-contained frontend in `app/frontend/index.html`
- Frontend calls `http://localhost:8000`
- No database and no authentication

## API Routes

| Method | Path               | Description                       |
| ------ | ------------------ | --------------------------------- |
| GET    | `/health`          | Service health                    |
| POST   | `/tasks`           | Create a task (HTTP 201)          |
| GET    | `/tasks`           | List and filter tasks             |
| GET    | `/tasks/{task_id}` | Retrieve one task                 |
| PATCH  | `/tasks/{task_id}` | Partial update                    |
| DELETE | `/tasks/{task_id}` | Delete a task (HTTP 204, no body) |

`GET /tasks` accepts optional `q`, `status`, `priority`, and `overdue` query
parameters, which apply together.

## Running Locally

Set up the environment:

```bash
python3.11 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

Start the backend:

```bash
uvicorn app.main:app --reload --port 8000
```

Serve the frontend in another terminal:

```bash
python3 -m http.server 5500 --directory app/frontend
```

Then open http://localhost:5500 while the backend is running on port 8000.

Interactive API documentation is generated from the route definitions and served at:

- http://localhost:8000/docs
- http://localhost:8000/redoc

## Testing and CI

```bash
python -m pytest -v --tb=short
```

The latest verified local run passed all 29 tests.

GitHub Actions (`.github/workflows/ci.yml`) runs the same command on Python 3.11 for
every branch push and for pull requests targeting `main`. A failing test fails the
workflow.

## Docker

The `Dockerfile` uses a multi-stage Python 3.11-slim build: a builder stage installs
dependencies into a virtual environment, and a separate runtime stage copies only that
environment and the application code. The container runs as a non-root `app` user and
defines a health check against `/health`. It serves the FastAPI backend only — not the
browser frontend, which is served separately as shown above.

```bash
docker build -t task-tracker-api .
docker run --rm -d --name task-tracker-api -p 8000:8000 task-tracker-api
curl http://127.0.0.1:8000/health
docker stop task-tracker-api
```

## AI-Assisted Development

This project was built with AI assistance under direct human ownership.

Kayan defined the requirements, feature decisions, and acceptance criteria. Claude Code
in VS Code supported iterative implementation, testing, documentation, debugging, code
review, and security analysis. The final work remained human-reviewed: Kayan
inspected the diffs, ran the full test suite, exercised the application manually, and
verified the Docker build and the `/health` endpoint.

## Documentation

- [Architecture](docs/architecture.md) — system design and component boundaries
- [Security review](docs/security-review.md) — threat surface and findings
- [Release evidence](docs/release-evidence.md) — verification record for the release
- [Final AI review](docs/final-ai-review.md) — AI review pass and accepted/rejected findings
- [AI usage](docs/ai-usage.md) — how AI assistance was applied
- [Mid-course docs](docs/midcourse/) — ADR, user stories, prompt log, verification
- [Module 4 evidence](docs/module4/) — Claude Code, CI, and Docker evidence

## Current Limitations

- In-memory storage resets on restart
- No authentication or multi-user isolation
- The frontend API URL is configured for local development
- The Docker image serves only the backend
- This is a learning and portfolio project, not presented as a deployed production service
