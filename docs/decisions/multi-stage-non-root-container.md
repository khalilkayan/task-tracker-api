# Multi-Stage Docker Image with a Non-Root Runtime User

## Context

For Module 4 I needed to package the Task Tracker API's FastAPI backend
(`app/main.py`) into a container that anyone could build and run the same
way, without depending on my local Python 3.11 virtualenv setup. Before this
decision, `README.md` only documented running the backend locally with
`uvicorn app.main:app --reload --port 8000`. I wanted a container that would
run the exact same application in a repeatable way, but without dragging in
the build tooling I only need while installing dependencies, and without
running the process as root inside the container, since neither of those is
necessary once the app is actually running.

## Decision

I built the `Dockerfile` at the repository root as a multi-stage image. Both
stages start from `python:3.11-slim`. The first stage, named `builder`,
creates a virtual environment at `/opt/venv` and installs everything from
`requirements.txt` into it. The second stage, named `runtime`, starts from a
fresh `python:3.11-slim` image and copies in only two things: the
`/opt/venv` virtual environment from the builder stage, and the `app/`
directory from the build context. It creates a dedicated `app` user and
group, both with UID/GID `1000`, and switches to that user with `USER app`
before anything runs. It defines a `HEALTHCHECK` that calls
`http://127.0.0.1:8000/health` using Python's own `urllib.request`, so I
didn't need to install `curl` just for that. The final `CMD` runs
`uvicorn app.main:app --host 0.0.0.0 --port 8000`, with no `--reload`, since
that flag is for local development, not a built image.

One thing worth stating plainly: because the runtime stage's
`COPY --chown=app:app app/ ./app/` copies the entire `app/` directory,
`app/frontend/index.html` ends up inside the image too — even though the
container's `CMD` only starts the FastAPI backend and never serves that file
over HTTP.

## Alternatives Considered

**A single-stage container running as root.** This is the simplest possible
Dockerfile: one `FROM python:3.11-slim`, `pip install`, `COPY`, `CMD`, done.
I rejected it because it would leave pip's install layer sitting in the same
image that actually runs, and because running the app as the default root
user inside the container gives an attacker, or a bug, more privilege than
the process needs. Nothing about serving a FastAPI app with in-memory
storage requires root.

**A full Python base image or a development container with `--reload`.** I
considered just using `python:3.11` instead of `-slim`, and running with
`--reload`, since that's closer to how I run the app locally. I rejected
this because `--reload` exists to watch the filesystem for changes during
active development — it has no purpose in an image that's meant to be an
immutable, built artifact — and the full base image carries OS packages I
don't need at runtime just to make a local dev loop faster.

## Trade-offs

Choosing the multi-stage, non-root design over the simpler alternatives cost
me some things. The Dockerfile itself is longer and more complex than a
single-stage version — I have to think about what crosses the stage boundary
and what doesn't. The runtime image also has fewer debugging tools available
than a full base image would, since `python:3.11-slim` is intentionally
minimal. I would do this differently next time by checking exactly what
every COPY instruction puts into the image before documenting it, because I
initially overlooked that app/frontend is copied even though the container
does not serve it. And because nothing in the image is mounted from the
host, the image has to be rebuilt any time the dependencies or the
application files change — there's no live-reload path once it's packaged
this way.

## Consequences

After building the image and running it, I verified (see
`docs/module4/part-4-3-docker-evidence.md`) that `curl -i
http://127.0.0.1:8000/health` returned HTTP `200`, and that Docker's own
health status, checked with `docker inspect`, reported `healthy`. Running
`whoami` inside the container returned `app`, and `id` confirmed both the
UID and GID were `1000`, not `0`. `docker image inspect` reported the built
image at approximately `65.3 MiB`.

## Open Questions

I still don't have a firm answer on whether the dependencies in
`requirements.txt` should be pinned to specific versions rather than left
unpinned, which would make rebuilds more reproducible but also means I'd
have to remember to bump them deliberately. I also haven't decided whether
the GitHub Actions workflow in `.github/workflows/ci.yml` should build and
inspect the Docker image as part of CI, the way it currently only installs
dependencies and runs pytest. And since `app/frontend` is copied into the
image without ever being served, I'm not sure yet whether the frontend
should eventually get its own separate image, or its own build step,
instead of just riding along inside the backend image unused.
