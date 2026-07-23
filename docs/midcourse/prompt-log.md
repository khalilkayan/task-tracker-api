# AI Prompt Log

This file records the meaningful AI prompts used during the project, what the AI suggested, and what was accepted, edited, or rejected.

## Feature 1: Search and Combined Filters

## Feature 2: Due Dates and Overdue Filtering

### Prompt 1 — Inspect and plan the backend search feature

#### Prompt

Inspect the attached Task Tracker files before suggesting any code.

I am implementing Feature 1 of a graded AI-assisted coding project: search and combined filters.

Current behavior:
- GET /tasks already supports optional status and priority filters.
- Tasks are stored in memory.
- Tests use the existing synchronous TestClient and reset storage before every test.

Required backend behavior:
- Extend the existing GET /tasks endpoint with an optional q query parameter.
- Search task title and description.
- Matching must be case-insensitive.
- Partial text matches must work.
- Search must combine with the existing status and priority filters.
- Missing, empty, or whitespace-only q should behave like no search filter.
- No matches must return HTTP 200 with [].

Constraints:
- Do not create a new endpoint.
- Do not change the task models.
- Do not modify the frontend yet.
- Do not add dependencies.
- Do not edit any files in this response.
- Do not rewrite complete files.

First, provide only:
1. The exact files and functions that need changes.
2. A small implementation plan in order.
3. The tests that should be added.
4. Any assumptions or risks I should review.

Keep the response focused and under 15 bullet points.

#### AI response summary

Copilot identified `app/main.py`, `app/storage.py`, and `tests/test_tasks.py` as the only files needed for the backend search feature. It proposed adding an optional `q` parameter to the existing `GET /tasks` route, trimming and normalizing the value, and applying case-insensitive partial matching to task titles and descriptions. It also proposed tests for title search, description search, combined filters, whitespace-only search, and no-match behavior.

#### Decision

Accepted:
- Extend the existing `GET /tasks` endpoint.
- Add search logic inside `storage.get_all_tasks`.
- Search both title and description.
- Use case-insensitive partial matching.
- Treat blank or whitespace-only search as no filter.
- Keep the existing models and test infrastructure unchanged.

Edited:
- The suggested combined-filter test will be implemented in small focused tests rather than immediately creating one large test covering every filter combination.

Rejected:
- No major suggestion was rejected because the proposed plan stayed within the agreed scope.

Reason:
The response was grounded in the existing files, preserved the current architecture, and did not propose unnecessary dependencies or rewrites.

### Prompt 2 — Rewrite a weak prompt and add two search tests

#### Weak prompt

Add search tests to my task app.

#### Stronger prompt

Add exactly two focused pytest tests to `tests/test_tasks.py`:

1. `test_list_tasks_search_matches_title_case_insensitively`
2. `test_list_tasks_search_matches_description_case_insensitively`

Each test must create a matching and non-matching task using the existing synchronous TestClient. The tests must prove partial, case-insensitive matching, assert HTTP 200, and verify that only the intended task is returned.

The AI was constrained to modify only `tests/test_tasks.py`, preserve existing tests and fixtures, and avoid implementing the search feature itself.

#### AI response summary

Copilot added two focused endpoint tests. The first searches a partial mixed-case value against a task title. The second searches a partial mixed-case value against a task description. Each test creates one matching task and one non-matching task and verifies that only the matching task is returned.

Copilot then ran the existing test file. The result was 2 failed and 16 passed because the API did not yet implement the `q` search parameter.

#### Decision

Accepted:
- Both generated tests.
- The existing TestClient style.
- Creating matching and non-matching tasks inside each test.
- Assertions for HTTP 200, one result, and the matching task ID.

Edited:
- No manual edits were required after inspection.

Rejected:
- No application fix was accepted at this stage because the purpose was to capture the expected failing tests before implementation.

Reason:
The two failures correctly demonstrated that the tests protected behavior that did not yet exist. This created a clear test-first red phase.

### Prompt 3 — Implement the smallest backend search change

#### Prompt summary

Copilot was asked to implement the smallest backend change needed to make the two failing search tests pass.

The requirements were to:

- Add an optional `q` parameter to the existing `GET /tasks` endpoint.
- Pass `q` into `storage.get_all_tasks`.
- Search title and description using partial, case-insensitive matching.
- Treat missing, empty, or whitespace-only `q` as no search filter.
- Preserve combinations with status and priority.
- Modify only `app/main.py` and `app/storage.py`.
- Preserve existing tests, models, frontend code, and dependencies.
- Show the focused diff before applying it.

#### AI response summary

Copilot added `q` to the existing `list_tasks` route and passed it to `storage.get_all_tasks`. It added text filtering before the existing status and priority filters.

The first generated version normalized values with `.lower()` and directly called `.lower()` on `task.description`. It also applied the change before showing the requested diff.

#### Decision

Accepted:
- Adding `q` to the existing `GET /tasks` endpoint.
- Passing `q` into `storage.get_all_tasks`.
- Keeping search inside the existing storage filtering function.
- Preserving the existing status and priority filters.
- Treating blank or whitespace-only search as no filter.

Edited:
- Replaced `.lower()` with `.casefold()` for case-insensitive matching.
- Replaced direct use of `task.description.lower()` with `(task.description or "").casefold()` because description is optional and may be null.

Rejected:
- The unsafe direct call to `.lower()` on an optional description.
- The AI workflow of applying changes before showing the requested diff.

Reason:
The implementation was small and correctly structured, but manual review found a possible runtime error. Correcting the optional-description handling made the feature safe for all valid task data.

#### Verification

Targeted search tests passed:

`2 passed, 16 deselected`

The complete test suite passed:

`18 passed, 1 warning in 0.04s`
