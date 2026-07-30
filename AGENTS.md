# Task Tracker — Codex Instructions

These instructions apply to the entire repository.

## Stack

Use only stack details verified from repository files:

- Python 3.11.
- FastAPI backend served by Uvicorn.
- Pydantic v2 models and validation.
- In-memory Python task storage; there is no database.
- pytest and httpx for automated API testing.
- Vanilla HTML, CSS, and JavaScript frontend with no build step or package manager.
- GitHub Actions continuous integration using Python 3.11.
- A multi-stage Docker build based on `python:3.11-slim`, with the application running as a non-root user.
- Declared Python dependencies are FastAPI, Uvicorn with standard extras, Pydantic, python-dotenv, pytest, and httpx.

Do not assume unverified frameworks, services, tools, or infrastructure are available.

## Verified commands

The following commands are documented by the repository. Do not invent substitute setup, run, test, lint, formatting, or deployment commands.

Setup:

```bash
python3.11 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

Run the backend:

```bash
uvicorn app.main:app --reload --port 8000
```

Run the frontend in a second terminal:

```bash
python3 -m http.server 5500 --directory app/frontend
```

Run the pytest suite:

```bash
python -m pytest -v --tb=short
```

Run the standalone validation script, which is not collected by pytest:

```bash
PYTHONPATH=. python tests/verify_a.py
```

No linter or formatter is configured in the repository. Do not invent lint or formatting commands.

Do not run any command without explicit approval. Request permission for one action at a time.

## Project rules

- Task statuses are `ToDo`, `InProgress`, and `Done`.
- Priorities are `Low`, `Medium`, and `High`.
- The verified status transitions are:
  - `ToDo` → `InProgress`
  - `InProgress` → `Done`
  - `Done` → `InProgress`
- Preserve existing API paths, response shapes, and status codes unless explicitly asked.
- Do not add authentication, a database, deployment features, or new dependencies.
- Module 5 is primarily evaluation, security review, governance, planning, and reflection.
- Prefer read-only analysis first.
- Only create or edit files under `docs/` unless the user explicitly approves another path.
- `AGENTS.md` itself is the one approved repository-root exception.
- Do not edit `app/`, `tests/`, CI, Docker configuration, or frontend files unless explicitly approved.
- Do not run destructive commands.
- Do not change task business rules without explicit approval.
- Do not make unrelated changes.

## Review expectations

- State which files were read.
- Ground every technical claim in repository evidence.
- Say clearly when a claim cannot be verified.
- Distinguish repository evidence from assumptions, recommendations, and user-provided requirements.
- Show the complete proposed diff before applying any change.
- Wait for explicit approval before writing files or running commands.
- Request permission one action at a time.
- Keep proposed work within the approved path and scope.
- After an approved change, report exactly which files changed and which approved verification commands were run.
