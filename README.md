# Task Tracker API

A small full-stack task-management project built with FastAPI, in-memory Python storage, pytest, and a vanilla HTML, CSS, and JavaScript Kanban board.

This mid-course extension adds two end-to-end features:

1. Search and combined task filters
2. Due dates and overdue filtering

## Features

- Create, read, update, and delete tasks
- ToDo, InProgress, and Done Kanban columns
- Validated task-status transitions
- Search by task title or description
- Filter by priority
- Combine search, priority, and overdue filters
- Add, change, or remove optional due dates
- Display due dates and Overdue indicators on task cards
- Filter for unfinished overdue tasks
- Responsive vanilla JavaScript frontend
- Automated API tests with pytest

## Technology

- Python
- FastAPI
- Pydantic
- pytest
- HTML
- CSS
- JavaScript

## Project structure

```text
.github/
└── workflows/
    └── ci.yml

app/
├── frontend/
│   └── index.html
├── business_rules.py
├── main.py
├── models.py
└── storage.py

docs/
├── midcourse/
│   ├── mini-adr.md
│   ├── prompt-log.md
│   ├── reflection.md
│   ├── user-stories.md
│   └── verification.md
└── module4/
    ├── part-4-1-claude-code-evidence.md
    ├── part-4-2-ci-evidence.md
    └── part-4-3-docker-evidence.md

tests/
├── conftest.py
├── test_tasks.py
└── verify_a.py

.dockerignore
CLAUDE.md
Dockerfile
```

## Local setup

```bash
python3.11 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

## Run the backend locally

```bash
uvicorn app.main:app --reload --port 8000
```

## Run the frontend

In a second terminal:

```bash
python3 -m http.server 5500 --directory app/frontend
```

Open http://localhost:5500 while the backend is running on port 8000.

## API documentation

While the backend is running (locally or in the Docker container), FastAPI
serves interactive API documentation, generated automatically from the
route definitions in `app/main.py`, at:

- `http://localhost:8000/docs` — Swagger UI
- `http://localhost:8000/redoc` — ReDoc

## Run the tests

```bash
python -m pytest -v --tb=short
```

As of the final-project baseline verification, all 29 tests passed. Test count and
results can change as the suite evolves — rerun the command above for the
current result; the authoritative status for any given commit is the
GitHub Actions run defined at `.github/workflows/ci.yml`.

Run the standalone validation script separately:

```bash
PYTHONPATH=. python tests/verify_a.py
```

## Run with Docker

The `Dockerfile` at the repository root builds a container image for the
backend using a multi-stage build: a `builder` stage installs dependencies
into a virtual environment, and a separate `runtime` stage copies only
that virtual environment and the `app/` directory (including
`app/frontend/`), running the application as a non-root `app` user. The
image also defines a Docker `HEALTHCHECK` that polls `/health` from
inside the container.

The container's `CMD` starts only the FastAPI backend
(`uvicorn app.main:app`); it does not serve `app/frontend/index.html`
over HTTP, even though that file is present inside the image. To use the
browser frontend, continue to serve it separately with the command
documented under "Run the frontend" above.

Build the image:

```bash
docker build -t task-tracker-api:module4 .
```

Run it, mapping container port 8000 to the host:

```bash
docker run -d --name task-tracker-api -p 8000:8000 task-tracker-api:module4
```

Check that it's healthy:

```bash
curl http://localhost:8000/health
```

Stop and remove the container:

```bash
docker stop task-tracker-api
docker rm task-tracker-api
```

## Continuous integration

GitHub Actions is configured at `.github/workflows/ci.yml`. The `test` job
runs on `ubuntu-latest` with Python 3.11, and triggers:

- on every push, to any branch
- on pull requests targeting `main`

It installs dependencies from `requirements.txt` and runs the test suite
with:

```bash
python -m pytest -v --tb=short
```

A failing test fails the workflow.

## Documentation conventions

- Public functions and methods (names that do not start with an underscore)
  use Google-style docstrings — a summary, `Args`, `Returns`, and, where
  applicable, `Raises`. Route handlers in `app/main.py` also include a concise
  `Example`.
- Private, underscore-prefixed helpers (for example
  `storage._is_task_overdue` and `storage._reset`) are internal implementation
  details and are intentionally not required to have docstrings.
- Docstring `Example` and `Raises` content must match the actual
  implementation — no invented fields, routes, query parameters, statuses, or
  behavior.

## Documentation

Planning, architecture decisions, prompt records, verification evidence,
and reflection material for the mid-course project are in
`docs/midcourse/`. Evidence for the Module 4 work (Claude Code usage, CI,
and Docker) is in `docs/module4/`.

- [Technical decision: multi-stage non-root container](docs/decisions/multi-stage-non-root-container.md)
- [Module 4 tool reflection](docs/module4/part-4-6-tool-reflection.md)

## Final Project

Branch reviewed: `final-project`

### What this submission demonstrates

- The existing Task Tracker app still runs inside the intended course scope.
- CI runs the pytest suite on push and pull request.
- The Docker image builds and runs with `/health` returning HTTP 200.
- AI review, security, and ownership evidence is recorded in `docs/`.

### How to run locally

Backend:

```bash
python3.11 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
