# Comments Feature Plan

This is a planning document only. It does not authorize or include implementation changes.

Repository evidence reviewed: `AGENTS.md`, `app/models.py`, `app/main.py`, `app/storage.py`, `tests/conftest.py`, `tests/test_tasks.py`, `tests/verify_a.py`, `app/frontend/index.html`, and `README.md`. An inventory of `app/` confirmed that the repository has no separate route files; all current routes are defined in `app/main.py`.

## 1. Data Model

- **Repository evidence:** `app/models.py` separates client input (`TaskCreate` and `TaskUpdate`) from server responses (`TaskResponse`). Input models use Pydantic v2, set `extra="forbid"`, and normalize and validate required task text with a `field_validator`. `TaskResponse` represents UUIDs as strings and generates timezone-aware UTC datetimes with `datetime.now(timezone.utc)`.
- **Plan:** Add a `CommentCreate` input model in `app/models.py` containing only `author` and `body`. Do not accept `id`, `task_id`, or `created_at` from the request body because the existing task models keep server-managed fields out of creation input.
- **Plan:** Require `author`, strip surrounding whitespace, reject an empty post-strip value, and enforce a post-normalization length of 1 to 100 characters. This follows `TaskCreate.validate_title`.
- **Plan:** Require `body`, reject empty or whitespace-only content, and enforce a length of 1 to 2000 characters. Whether surrounding body whitespace should be stripped or retained needs confirmation because the repository has no multiline-content validation precedent.
- **Plan:** Add a `CommentResponse` model containing `id: str`, `task_id: str`, `author: str`, `body: str`, and `created_at: datetime`.
- **Plan:** Generate `id` with the same stringified `uuid4()` pattern and `created_at` with the same timezone-aware UTC pattern used by `TaskResponse`. Populate `task_id` from the route path on the server.
- **Constraint:** Do not add authentication or infer an authenticated identity. `AGENTS.md` prohibits adding authentication, so `author` remains a validated client-supplied display string.

### My Critique

- **Label: Right.** The proposed `CommentCreate` and `CommentResponse` split follows the existing `TaskCreate`/`TaskResponse` pattern and correctly keeps `id`, `task_id`, and `created_at` server-managed.
- The validation approach also matches the repository’s existing style, while correctly leaving body-whitespace behavior as an open decision.

## 2. API Routes

- **Plan:** Add `POST /tasks/{task_id}/comments` in `app/main.py`, returning `CommentResponse` with HTTP 201.
- **Existing pattern followed:** `POST /tasks` uses a typed input model, a `response_model`, and `status.HTTP_201_CREATED`. The nested path also follows the existing `/tasks/{task_id}` resource convention.
- **Plan:** Before storing a comment, verify the parent with `storage.get_task_by_id(task_id)`. Return HTTP 404 with the existing task-not-found detail convention when the task does not exist.
- **Plan:** Add `GET /tasks/{task_id}/comments`, returning `list[CommentResponse]` with HTTP 200. An existing task with no comments should return `[]`.
- **Existing pattern followed:** `GET /tasks` returns a typed list and uses an empty list for no matches; `GET /tasks/{task_id}` establishes explicit 404 handling for a missing task.
- **Plan:** Keep the comment handlers in `app/main.py` because all current routes are defined there and no router modules exist. Use FastAPI response metadata and concise route docstrings consistent with the current task handlers.
- **Plan:** Ensure comments from one task cannot be returned through another task’s nested route.
- **Scope:** Do not add comment update, individual retrieval, or deletion routes unless those behaviors are explicitly selected; the requested create-and-list relationship does not define them.

### My Critique

- **Label: Right.** The proposed nested routes, status codes, and missing-task handling follow the repository’s existing API conventions.
- Keeping comment creation and listing in `app/main.py` also matches the current structure, while leaving edit and delete routes out of scope unless they are explicitly required.

## 3. Tests

- **Repository evidence:** `tests/conftest.py` provides a synchronous FastAPI `TestClient`, creates tasks through the public API, and resets storage before and after every test. `tests/test_tasks.py` uses behavior-focused test names and asserts exact status codes and response fields. `tests/verify_a.py` separately checks model restrictions such as rejection of server-managed fields.
- **Plan:** Add focused comment API coverage to the existing `tests/test_tasks.py`, using the existing `client` and `created_task` fixtures rather than directly populating storage. This follows the repository’s current convention of keeping API behavior tests in that file.
- **Creation tests:** Verify HTTP 201; echoed `task_id`, `author`, and `body`; a nonempty UUID string; and a parseable UTC `created_at` value.
- **Validation tests:** Cover missing, empty, whitespace-only, exact maximum, and over-maximum values for both `author` and `body`.
- **Protection tests:** Verify that client-supplied `id`, `task_id`, `created_at`, and unknown fields produce HTTP 422, following the repository’s `extra="forbid"` convention.
- **Association tests:** Verify HTTP 404 when creating or listing comments for a nonexistent task and verify that comments are isolated by task.
- **Listing tests:** Verify an empty list for an existing task with no comments, all comments for one task, response shape, and the selected deterministic ordering.
- **Deletion tests:** Once task-deletion behavior is decided, verify either cascade removal or the explicitly chosen alternative without changing the existing successful task-delete response of HTTP 204.
- **Isolation:** Extend `storage._reset()` so the autouse fixture continues to prevent state leakage across tests.
- **Standalone script:** Decide whether `tests/verify_a.py` remains limited to its current task-model checks or gains comment-model checks; the repository does not establish a rule for extending this script with every feature.
- **Verification:** During implementation, run only the documented commands after approval: `python -m pytest -v --tb=short`, followed separately by `PYTHONPATH=. python tests/verify_a.py` if that script changes.

### My Critique

- **Label: Right.** The test plan follows the repository’s existing `TestClient` and fixture setup, keeps API behavior coverage in `tests/test_tasks.py`, and checks the main validation and task-association cases.
- Extending `storage._reset()` for comments also correctly preserves the current test-isolation pattern.

## 4. Frontend Changes

- **Repository evidence:** `app/frontend/index.html` contains all frontend HTML, CSS, and JavaScript. It renders task cards from an in-memory `tasks` array, uses event delegation on the board, escapes rendered values with `escapeHtml`, uses `fetch` for API calls, and displays parsed server errors through `parseResponsePayload` and `getErrorDetail`.
- **Plan:** Add a comments action to each task card and open a dedicated comments view or modal for the selected task. A separate comments modal is the initial recommendation because the existing task modal is already responsible for task creation and editing.
- **Existing pattern followed:** Reuse the current modal structure, open/close behavior, error banner, field-error treatment, and Escape-key behavior rather than introducing a new frontend framework or build step.
- **Plan:** Fetch `GET /tasks/{task_id}/comments` when the comments view opens, with distinct loading, empty, ready, and error states.
- **Plan:** Render each comment’s author, body, and formatted creation time. Pass author and body through `escapeHtml` before inserting them into generated markup.
- **Plan:** Add a form with required author and body controls, HTML maximum-length hints, accessible labels, and server-error display. Submit it to `POST /tasks/{task_id}/comments`.
- **Existing pattern followed:** Reuse `API_BASE`, `encodeURIComponent`, `parseResponsePayload`, `getErrorDetail`, and the current refresh-after-success approach.
- **State plan:** Keep comment state associated with the selected task rather than adding comments to task API response objects, because current task response shapes should remain unchanged.
- **Responsive and accessibility plan:** Extend the existing responsive modal rules, focus the first comment field on open, preserve keyboard closing, and use an appropriate live or alert region for loading and submission failures.
- **Documentation plan:** During implementation, update `README.md` feature and API documentation without changing its verified setup, run, or test commands.

### My Critique

- **Label: Right.** The frontend plan follows the repository’s existing single-file HTML/CSS/JavaScript structure and reuses the current modal, fetch, error-handling, and escaping patterns.
- The proposed comments UI also keeps the existing task response shape unchanged and treats the exact interaction design as a product decision rather than an established repository convention.

## 5. Migration or Storage Notes

- **Repository evidence:** `app/storage.py` uses a module-level `dict[str, TaskResponse]`; there is no database or persistence layer. `README.md` also describes storage as in-memory.
- **Plan:** Add a separate in-memory comment dictionary keyed by comment ID, storing `CommentResponse` values. This mirrors the existing `_tasks` dictionary rather than embedding mutable comment lists into `TaskResponse`.
- **Plan:** Add storage operations to create a comment and list comments filtered by `task_id`. Route handlers should continue to own HTTP 404 decisions, as current storage functions return values such as `None` or `False` rather than raising HTTP exceptions.
- **Plan:** Update `storage._reset()` to clear both task and comment collections.
- **Deletion recommendation:** Remove a task’s comments when that task is successfully deleted so the in-memory store cannot retain orphaned comments. This requires explicit confirmation because current files contain no relationship-deletion precedent.
- **Ordering recommendation:** Return comments oldest-first using `created_at` with a stable ID tie-breaker, rather than relying implicitly on dictionary insertion order.
- **Migration:** No schema or data migration is required because the repository has no database and no durable data.
- **Persistence limitation:** Comments, like tasks, will be lost when the process restarts. Durable storage is outside the verified stack and outside this feature.
- **Dependencies:** No new dependency is needed; UUID generation, UTC datetimes, Pydantic, and FastAPI patterns already exist in the repository.

### My Critique

- **Label: Right.** The storage plan matches the repository’s current in-memory design by proposing a separate comment dictionary and keeping HTTP-specific behavior out of the storage layer.
- Updating `storage._reset()` and explicitly deciding cascade deletion and comment ordering are also consistent with the existing test and storage patterns.

## 6. Open Questions

- Should deleting a task cascade-delete its comments? The recommendation is yes, but the repository does not define relationship deletion behavior.
- Should comment body whitespace be stripped, or only checked for non-whitespace content while preserving the submitted formatting?
- Are comments immutable, or should later work include edit and delete operations? Those operations are not present in the current requirement.
- Should the frontend use a dedicated modal, an expandable area inside each task card, or a future task-detail view? No existing detail-view pattern answers this.
- Should the browser remember the last entered author locally, or require it for every comment? No preference-storage convention exists.
- Is oldest-first ordering acceptable, or should newest comments appear first? The requirement does not specify ordering.

### My Critique

- **Label: Right.** The open questions correctly identify decisions that the repository does not currently answer, including deletion behavior, comment ordering, whitespace handling, and the exact frontend interaction.
- Keeping these unresolved instead of inventing answers is appropriate for a planning document and makes the remaining product decisions clear.

## Generic vs Repo-Grounded Codex Comparison

**Biggest difference:** The generic plan described sensible feature steps in abstract terms, while the repo-grounded plan tied those decisions to the actual files, models, storage structure, test setup, and frontend conventions already used in this project.

**Plan I would hand to a teammate:** I would hand the repo-grounded plan to a teammate because it references the actual project structure and existing conventions, making it much more actionable and less likely to introduce unnecessary changes.

**Where the generic plan was still useful:** The generic plan was still useful for identifying the basic feature shape, such as needing a comment model, create/list operations, validation, tests, frontend support, and documentation before looking at repository-specific details.

**Where repo grounding mattered most:** Repo grounding mattered most when deciding exactly where the models, routes, storage logic, tests, and frontend changes would belong, because those decisions depend on the project’s existing structure and conventions.
