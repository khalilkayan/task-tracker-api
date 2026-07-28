# Part 4.4 — Documentation Evidence

## Objective

- Generate accurate documentation without changing application behavior.
- Add public-function docstrings, update README, inspect API docs, and record
  AI inaccuracies caught by human review.

## Documentation scope

- 14 public functions or methods received Google-style docstrings.
- `app/models.py`:
  - `TaskCreate.validate_title`
  - `TaskUpdate.validate_title`
- `app/business_rules.py`:
  - `validate_status_transition`
- `app/storage.py`:
  - `add_task`
  - `get_all_tasks`
  - `get_task_by_id`
  - `update_task`
  - `delete_task`
- `app/main.py`:
  - `health_check`
  - `create_task`
  - `list_tasks`
  - `get_task`
  - `update_task`
  - `delete_task`
- `storage._is_task_overdue` and `storage._reset` were intentionally excluded
  because they are private underscore-prefixed helpers.

## Docstring accuracy

- The model validators (`TaskCreate.validate_title`, `TaskUpdate.validate_title`)
  document stripping of the input, `None` pass-through behavior (for the
  `TaskUpdate` variant), the exact return values, and only the actual
  `ValueError` conditions each function body raises — no `HTTPException` is
  attributed to either validator.
- `validate_status_transition` documents its explicit `HTTPException` with
  status code 422, raised only when the `(current, new)` pair is not a member
  of `VALID_TRANSITIONS`.
- The `storage` functions document exact filtering behavior (`get_all_tasks`),
  missing-task behavior (`get_task_by_id`, `update_task` returning `None`),
  update semantics (`update_task` applying only explicitly-set fields), and
  delete semantics (`delete_task` returning `True`/`False`) — without
  inventing any HTTP exceptions, since none of these functions raise one.
- The route handlers in `app/main.py` each include a summary, `Args`,
  `Returns`, the actual `Raises` conditions present in the function body, and
  a concise `Example`.
- For `update_task` in `app/main.py`, the request-validation 422 (FastAPI/
  Pydantic parsing failures) is explicitly distinguished in the docstring from
  the business-rule 422 propagated from `validate_status_transition`.

## README changes

`README.md` now includes:

- current project structure, including `.github/workflows/ci.yml`,
  `docs/module4/`, `.dockerignore`, `CLAUDE.md`, and `Dockerfile`
- Python 3.11 local setup instructions
- backend and separate frontend commands, documented independently from the
  Docker container instructions
- `/docs` and `/redoc` interactive API documentation
- the verified test command: `python -m pytest -v --tb=short`
- Docker build, run, health-check, stop, and remove commands
- a description of the multi-stage build, the non-root `app` user, and the
  Docker `HEALTHCHECK`
- an accurate statement that `app/frontend` is copied into the image, while
  the container `CMD` starts only the FastAPI backend
- GitHub Actions triggers (push to any branch, pull requests targeting
  `main`) and the test command it runs
- documentation conventions (Google-style docstrings for public functions,
  private helpers intentionally undocumented, examples/raises must match code)
- `docs/midcourse/` and `docs/module4/` locations

## OpenAPI metadata correction

- Swagger initially omitted explicit handler 404 responses from its response
  tables even though the docstrings described them accurately.
- Metadata-only decorator changes documented 404 for `GET`, `PATCH`, and
  `DELETE` `/tasks/{task_id}`.
- `PATCH` 422 now uses `oneOf` for:
  - `#/components/schemas/HTTPValidationError`
  - an object requiring a string `detail` property
- No function body, route path, success status, response model, exception
  message, or application rule changed.

## Human spot checks

Three implementations were manually compared against their docstrings:

1. **`TaskUpdate.validate_title`** — verified that the code returns `None`
   unchanged when `value is None`, and otherwise strips the input and raises
   `ValueError` for an empty or over-200-character result, matching the
   docstring's `Args`, `Returns`, and `Raises` exactly.
2. **`storage.get_all_tasks`** — verified that the `q`, `status`, `priority`,
   and `overdue` filters are applied sequentially with AND semantics, that
   `q` uses a case-insensitive substring match skipped when blank, and that
   `overdue` only filters when it is exactly `True`, matching the docstring.
3. **`main.update_task`** — verified that the two explicit 404 raises and the
   propagated 422 from `validate_status_transition` (scoped to only when
   `payload.status` is supplied) match the `Raises` section, and that the
   422 is not conflated with FastAPI/Pydantic's own request-validation 422.

## Coverage verification

- All 14 public functions reported `DOCSTRING`.
- `_is_task_overdue` reported `NO DOCSTRING`.
- `_reset` reported `NO DOCSTRING`.
- This exactly matched the intended scope.

## Swagger and schema verification

- All six routes appeared: `GET /health`, `POST /tasks`, `GET /tasks`,
  `GET /tasks/{task_id}`, `PATCH /tasks/{task_id}`, `DELETE /tasks/{task_id}`.
- Expected schemas appeared: `HealthResponse`, `TaskCreate`, `TaskResponse`,
  `TaskUpdate`, `TaskStatus`, `TaskPriority`, `HTTPValidationError`,
  `ValidationError`.
- `POST /tasks` showed the `TaskCreate` request schema, defaults of `ToDo`
  and `Medium`, success status 201 with a `TaskResponse` body, and the
  framework-generated 422.
- `PATCH /tasks/{task_id}` showed 200, 404, and the combined 422 description.

## Direct OpenAPI verification

```
HTTPValidationError component: True
GET responses: ['200', '404', '422']
PATCH responses: ['200', '404', '422']
DELETE responses: ['204', '404', '422']
PATCH 422 schema: {'oneOf': [{'$ref': '#/components/schemas/HTTPValidationError'}, {'type': 'object', 'required': ['detail'], 'properties': {'detail': {'type': 'string'}}}]}
```

## Runtime endpoint verification

```
/docs: 200
/redoc: 200
```

## Test verification

- `28 passed, 2 warnings`
- The warnings were the previously observed non-blocking deprecation
  warnings.

## Claim-vs-reality log

**Entry 1:**
- AI claimed app/frontend/index.html was not included in the Docker image.
- Dockerfile actually copies the entire app/ directory, including app/frontend.
- Resolution: corrected README to explain that the files are present, but the
  container CMD starts only FastAPI, so the frontend is served separately.

**Entry 2:**
- AI claimed a description-only custom responses[422] entry should preserve
  FastAPI's automatically generated HTTPValidationError schema.
- Framework behavior actually made that assumption unsafe because a custom
  422 response can replace the automatic operation response.
- Resolution: explicitly defined both response shapes with oneOf and inspected
  the generated OpenAPI dictionary to confirm the reference resolves.

## Human responsibility

Claude proposed documentation, but the human:

- reviewed every proposed change
- rejected truncated or corrupted proposals
- caught inaccurate claims
- compared docstrings with code
- ran tests
- inspected Swagger and ReDoc
- checked OpenAPI directly
- remained responsible for final approval

## Current uncommitted state

```
README.md             | 120 +++++++++++++++++++++++++++++++++----
app/business_rules.py |  14 +++++
app/main.py           | 156 +++++++++++++++++++++++++++++++++++++++++++++++--
app/models.py         |  26 +++++++++
app/storage.py        |  56 ++++++++++++++++++
5 files changed, 357 insertions(+), 15 deletions(-)
```

`git diff --check` produced no output.

## Summary

- Local documentation verification is complete.
- Commit, push, and final CI verification are still pending.
