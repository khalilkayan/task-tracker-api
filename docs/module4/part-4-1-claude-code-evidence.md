# Part 4.1 — Claude Code Evidence

Date: 2026-07-26  
Branch: `module-4`  
Repository: `task-tracker-api`

## 1. Claude Code setup

Claude Code was installed and authenticated successfully.

Verified setup:

- Claude Code version: `2.1.220`
- Working directory: `/Users/kayan/Desktop/task-tracker-api`
- Login method: Claude Pro account
- IDE: Connected to VS Code
- Permission mode: Manual approval
- Python environment: Python `3.11.9`

Before allowing edits, Claude was asked to confirm the repository identity, identify important files, and check whether `CLAUDE.md` existed.

Claude correctly identified the FastAPI Task Tracker repository and confirmed that no `CLAUDE.md` or repository-specific Claude settings existed.

No files were changed during this initial read-only setup check.

## 2. CLAUDE.md creation and verification

Claude Code `/init` created an initial `CLAUDE.md` draft.

The draft was manually reviewed against:

- `README.md`
- `requirements.txt`
- `app/main.py`
- `app/models.py`
- `app/storage.py`
- `app/business_rules.py`
- `app/frontend/index.html`
- `tests/conftest.py`
- `tests/test_tasks.py`
- `tests/verify_a.py`

The first draft required corrections, including:

- Exact Python and dependency information
- Backend command with port 8000
- Frontend command with port 5500
- Exact test commands
- CORS origins
- Exact status-transition rules
- Repository-specific do-not rules
- Joined-word formatting errors

During verification, a corrupted and duplicated section in `README.md` was discovered and repaired.

Verified commands documented in `README.md` and `CLAUDE.md`:

```bash
uvicorn app.main:app --reload --port 8000
python3 -m http.server 5500 --directory app/frontend
pytest -v
PYTHONPATH=. python tests/verify_a.py