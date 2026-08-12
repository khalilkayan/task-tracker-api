# Release Evidence

## Baseline

- Branch: `final-project`
- Date: August 11, 2026
- Local app run command: `uvicorn app.main:app --reload --port 8000`
- `/health` result: `HTTP/1.1 200 OK` with `{"status":"ok", ...}`
- Frontend check: Served the existing frontend with `python3 -m http.server 5500 --directory app/frontend`, opened `http://localhost:5500`, and manually confirmed that the Kanban board loaded and that creating and editing a task still worked while the backend was running.
- Test command: `python -m pytest -v --tb=short`
- Test result: `29 passed, 2 warnings in 0.07s`

## CI Evidence

- Workflow file: `.github/workflows/ci.yml`
- Latest run link or note: CI has run successfully on the `final-project` branch, including the final repository state. The latest verified final-branch run completed successfully with all 29 tests passing.
- Test command used by CI: `python -m pytest -v --tb=short`
- Python version: `3.11`
- Dependencies: installed with `python -m pip install -r requirements.txt`
- Shortcut check: no `continue-on-error`, no `|| true`, and pytest is not skipped.
- Trigger check: workflow runs on pushes to all branches and pull requests targeting `main`.

## Docker Evidence

- Build command: `docker build -t task-tracker-api .`
- Build result: successful.
- Run command: `docker run --rm -d --name task-tracker-final -p 8000:8000 task-tracker-api`
- `/health` check: `curl -i http://127.0.0.1:8000/health` returned `HTTP/1.1 200 OK` with `"status":"ok"`.
- Non-root check: `docker exec task-tracker-final id` returned `uid=1000(app) gid=1000(app) groups=1000(app)`.
- Runtime configuration check: `User=app Cmd=["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]`.
- No-baked-secrets check: searching `/app` in the running container for `.env` and `*.env` files returned no results.

## Documentation Claim-vs-Reality Log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| README test command `python -m pytest -v --tb=short` runs the full suite. | Fresh final-project local run. | Correct: 29 tests passed. | Updated the stale README test count from 28 to 29. |
| README says the Docker image runs the backend as a non-root `app` user and exposes `/health`. | Fresh Docker build/run, `docker exec ... id`, `docker inspect`, and `/health` request. | Correct. Container ran as UID/GID 1000 and `/health` returned HTTP 200. | None. |
| README says CI uses Python 3.11, installs `requirements.txt`, and runs pytest on pushes and pull requests to `main`. | Manual inspection of `.github/workflows/ci.yml`. | Correct. No dangerous shortcut such as `continue-on-error` or `|| true` was present. | None. |