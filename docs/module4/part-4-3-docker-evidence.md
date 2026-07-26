# Part 4.3 — Docker Evidence

Date: 2026-07-26  
Branch: `module-4`  
Repository: `task-tracker-api`

## 1. Docker setup

Docker Desktop was installed for Apple silicon and started successfully.

Verified environment:

- Architecture: `arm64`
- Docker CLI version: `29.6.2`
- Docker engine version: `29.6.2`
- Docker Desktop engine status: running
- Git branch: `module-4`
- Git status before implementation: clean

No Dockerfile or `.dockerignore` existed before Part 4.3 began.

## 2. Dockerfile creation

Claude Code first read:

- `CLAUDE.md`
- `requirements.txt`
- `app/main.py`

Claude proposed the full Dockerfile before creating it.

The proposal was manually reviewed and corrected to ensure that the complete Python health-check command appeared on one uninterrupted line.

The approved Dockerfile uses a multi-stage build.

### Builder stage

The builder stage:

- Uses `python:3.11-slim`
- Is named `builder`
- Creates a virtual environment at `/opt/venv`
- Adds `/opt/venv/bin` to `PATH`
- Copies `requirements.txt` before application source
- Upgrades pip using `--no-cache-dir`
- Installs the project dependencies using `--no-cache-dir`

Only dependency installation happens in this stage.

### Runtime stage

The runtime stage:

- Uses a fresh `python:3.11-slim` image
- Is named `runtime`
- Creates a group named `app` with GID `1000`
- Creates a non-root user named `app` with UID `1000`
- Does not create a home directory
- Copies only `/opt/venv` from the builder stage
- Sets `/app` as the working directory
- Copies the source package from `app/` into `/app/app/`
- Sets ownership of the application files to `app`
- Switches to `USER app` before the health check and application command

The runtime image does not copy tests, documentation, Git data, local virtual environments, or environment files.

### Runtime command

The Dockerfile exposes port `8000`.

The application command is:

`uvicorn app.main:app --host 0.0.0.0 --port 8000`

The command does not use `--reload`.

### Health check

The Docker health check:

- Requests `http://127.0.0.1:8000/health`
- Uses Python's standard-library `urllib.request`
- Does not require curl
- Runs every 30 seconds
- Uses a 5-second timeout
- Uses a 10-second start period
- Allows 3 retries before marking the container unhealthy

The health check runs after `USER app`, so it also runs without root privileges.

## 3. Dockerignore creation

Claude separately proposed `.dockerignore` before creating it.

The file excludes:

- `.git`
- `.github`
- `.gitignore`
- `.env`
- `.env.*`
- `venv/`
- `.venv/`
- Python bytecode and cache files
- pytest and coverage output
- `tests/`
- `docs/`
- `.claude/`
- `CLAUDE.md`
- build and distribution artifacts
- `*.egg-info/`

It deliberately does not exclude:

- `app/`
- `requirements.txt`
- `Dockerfile`

This reduces the Docker build context and provides defense in depth against accidentally copying local files, secrets, development artifacts, tests, or documentation into an image.

## 4. Manual file inspection

The Dockerfile and `.dockerignore` were inspected line by line before building.

Manual checks confirmed:

- Builder and runtime stages both use `python:3.11-slim`
- The virtual environment is created at `/opt/venv`
- Only `/opt/venv` crosses from the builder into the runtime stage
- Application source is copied into `/app/app/`
- The fixed user is named `app`
- `USER app` appears before `HEALTHCHECK` and `CMD`
- Port `8000` is exposed
- The Uvicorn command contains no `--reload`
- No secrets or credentials appear
- No Docker Compose configuration was added
- No Kubernetes configuration was added
- No Buildx configuration was added
- No deployment files were added
- No extra system packages such as curl were installed

`git diff --check` produced no formatting errors.

## 5. Image build

The image was built locally with:

`docker build -t task-tracker-api:module4 .`

Build result:

- All 16 build operations completed successfully
- The builder stage completed successfully
- The runtime stage completed successfully
- The image was tagged `task-tracker-api:module4`

The build context transferred approximately `72.54 kB`, showing that `.dockerignore` excluded unnecessary repository contents.

## 6. Container run

The container was started with:

`docker run -d --name task-tracker-api-module4 -p 8000:8000 task-tracker-api:module4`

Docker returned a container ID and showed:

- Container status: running
- Initial health status: `health: starting`
- Port mapping: host port `8000` to container port `8000`

After the health-check start period, the container became healthy.

## 7. Health verification

The running application was tested using:

`curl -i http://127.0.0.1:8000/health`

Response:

- HTTP status: `200 OK`
- Server: Uvicorn
- Content type: `application/json`
- Response body contained `"status":"ok"` and a UTC timestamp

Docker's own health status was checked using `docker inspect`.

Result:

`healthy`

This confirmed both direct endpoint access and Docker's internal health-check behavior.

## 8. Non-root verification

The container user was checked with:

`docker exec task-tracker-api-module4 whoami`

Result:

`app`

The full identity was checked with:

`docker exec task-tracker-api-module4 id`

Result:

`uid=1000(app) gid=1000(app) groups=1000(app)`

The image configuration was also inspected.

Result:

- Configured user: `app`
- UID and GID: `1000`
- Application does not run as root

## 9. Image configuration verification

Docker image inspection confirmed the configured application command:

`["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]`

The command contains no `--reload`.

Docker image inspection also confirmed the health-check command:

`["CMD","python","-c","import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=5)"]`

The health check uses only Python's standard library.

## 10. Image size

The canonical image size was measured using `docker image inspect`.

Result:

- Size: `65.3 MiB`
- Bytes: `68,492,851`

This is comfortably below the course's approximate 200 MB target.

Docker Desktop also displayed separate storage measurements:

- Disk usage: approximately `317 MB`
- Content size: approximately `68.5 MB`

The canonical image-inspection value was used for the verified image-size evidence.

## 11. Cleanup

After verification, the running container was stopped and removed.

Commands used:

- `docker stop task-tracker-api-module4`
- `docker rm task-tracker-api-module4`

A subsequent container listing confirmed that no stopped or running container with that name remained.

The local image was retained for evidence and possible later verification.

## 12. Commit and CI verification

The Docker files were committed as:

`129e5d6 — Containerize Task Tracker API`

Files committed:

- `Dockerfile`
- `.dockerignore`

The commit was pushed to the remote `module-4` branch.

GitHub Actions automatically ran the existing CI workflow.

Result:

- Workflow: `CI`
- Job: `test`
- Status: success
- All checkout, Python setup, dependency installation, and test steps passed

This confirmed that containerization did not break the existing application or test suite.

## 13. Claude explanation and human verification

After implementation, Claude was asked to explain the Docker configuration in read-only mode.

Claude correctly explained:

- The builder stage
- The runtime stage
- The non-root user
- The health check
- The application command
- The purpose of `.dockerignore`
- The absence of secrets, environment files, tests, documentation, reload mode, Docker Compose, Kubernetes, deployment files, and curl

Claude did not run Docker during that explanation.

All build, run, health, user, size, cleanup, Git and GitHub Actions checks were independently performed and verified by the human.

Claude proposed and explained the containerization, but the human remained responsible for inspecting the files, approving edits, building the image, running the container, checking `/health`, confirming the non-root user, measuring the image, reviewing CI, and deciding that Part 4.3 was complete.
