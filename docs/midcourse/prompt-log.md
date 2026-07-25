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

### Prompt 4 — Add remaining backend search tests

#### Prompt summary

Copilot was asked to add exactly three focused tests for:

- Whitespace-only search behaving like no filter
- No-match search returning HTTP 200 with an empty list
- Search combining with status and priority

The AI was restricted to modifying only `tests/test_tasks.py`.

#### AI response summary

Copilot generated the three requested tests. The first two correctly covered whitespace and no-match behavior.

The first version of the combined-filter test did not fully prove that the search parameter mattered because status and priority alone already isolated the expected task.

#### Decision

Accepted:
- The whitespace-only search test
- The no-match search test
- The overall structure of the combined-filter test
- Use of valid ToDo to InProgress transitions

Edited:
- Added another High-priority InProgress task that did not contain the search text
- This ensured the `q` filter was necessary for the test to pass

Rejected:
- The original combined-filter setup because it could pass even if search logic were ignored

Reason:
The revised test independently proves that search, status, and priority all participate in the combined result.

### Prompt 5 — Implement the Feature 1 frontend toolbar

#### Prompt summary

Copilot was asked to modify only `app/frontend/index.html` and add:

- A search input
- A priority filter
- A Search button
- A Clear Filters button
- A shared `buildTasksUrl()` helper using `URLSearchParams`
- Filter handlers that call the backend
- Filter preservation after task refreshes and failed drag-and-drop synchronization

The prompt explicitly prohibited frontend-only filtering, board rewrites, modal changes, drag-transition changes, new dependencies, and due-date functionality.

#### AI response summary

Copilot added a compact filter toolbar above the Kanban board, styled it consistently with the existing interface, and created `buildTasksUrl()` to construct backend query URLs.

It updated both task-list requests:

- The normal request in `fetchTasks()`
- The synchronization request after an invalid drag-and-drop attempt

It also added form submission, priority-change, and Clear Filters handlers.

#### Decision

Accepted:
- The toolbar HTML and focused CSS
- Backend-driven filtering
- URL construction with `URLSearchParams`
- Automatic refresh when priority changes
- Search form submission
- Clear Filters behavior
- Reusing the same filtered URL during failed drag synchronization

Edited:
- No manual code edits were required after reviewing the proposed frontend diff.

Rejected:
- No major suggestion was rejected because the implementation remained within the planned scope.

Reason:
The implementation preserved the existing Kanban rendering, modal behavior, drag-and-drop rules, and empty-column states while making the new backend search feature usable from the frontend.

## Feature 2: Due Dates and Overdue Filtering

### Prompt 1 — Inspect and plan the due-date feature

#### Prompt summary

Copilot was asked to inspect the existing backend, tests, and frontend before proposing any edits.

The required feature included:

- An optional date-only `due_date`
- Create, update, removal, and response support
- Invalid dates returning HTTP 422
- An `overdue=true` filter on the existing `GET /tasks` endpoint
- Overdue defined as due date before today and status not Done
- Due-date input, card display, overdue indicator, and overdue-only frontend control
- Preservation of all existing behavior and architecture

#### AI response summary

Copilot identified `app/models.py`, `app/storage.py`, `app/main.py`, `tests/test_tasks.py`, and `app/frontend/index.html` as the relevant files.

It proposed adding the field to all task models, calculating overdue status in the backend, extending the existing list route, adding backend tests, and integrating the feature into the existing modal, cards, and filter toolbar.

#### Decision

Accepted:
- Use an optional date-only due date.
- Add the field to create, update, and response models.
- Extend the existing `GET /tasks` route with an overdue parameter.
- Calculate overdue at request time.
- Keep the current FastAPI, Pydantic, in-memory storage, pytest, and vanilla frontend architecture.
- Add the date input, card display, overdue indicator, and overdue-only filter.

Edited:
- Use Pydantic's built-in Python `date` parsing before considering custom validation.
- Treat `overdue=true` as the only value that enables overdue-only filtering; false or omitted means no overdue filter.
- Split the proposed broad overdue test into smaller focused tests.
- Use dates relative to `date.today()` in tests instead of fixed calendar dates.
- Avoid changing storage creation and update functions unless tests prove that their existing generic behavior is insufficient.
- Avoid modifying frontend functions that do not actually require changes.

Rejected:
- Adding unnecessary custom date validation before testing Pydantic's built-in behavior.
- One large test covering every overdue scenario.
- Unnecessary changes to functions already capable of carrying new model fields generically.

Reason:
The AI plan identified the correct architecture, but review reduced unnecessary code and produced more focused, stable tests.

### Prompt 2 — Add initial due-date regression tests

#### Prompt summary

Copilot was asked to add exactly three tests before implementing due-date support:

- Creating a task with a valid future due date
- Creating a task without a due date and receiving `due_date: null`
- Adding, changing, and removing a due date through PATCH

Dates were calculated relative to `date.today()` so the tests would remain valid over time.

#### AI response summary

Copilot added the requested datetime imports and three focused tests to `tests/test_tasks.py`.

The tests used the existing synchronous TestClient pattern and verified that unrelated task fields remained unchanged during due-date updates.

#### Decision

Accepted:
- All three generated tests
- Relative future dates using `date.today()` and `timedelta`
- Explicit PATCH removal using `{"due_date": None}`
- Assertions that the title remains unchanged

Edited:
- No manual edits were required after reviewing the test logic

Rejected:
- No application implementation was accepted at this stage because the tests were intentionally added before the feature

Process note:
- Copilot applied the changes before waiting for approval, despite being asked to show the diff first

Reason:
The tests are focused, stable, and clearly demonstrate the missing create, response, and partial-update behavior.

### Prompt 3 — Implement optional due-date model support

#### Prompt summary

Copilot was asked to make the smallest application change required to pass the three initial due-date tests.

The requested change was limited to:

- Importing Python's `date` type
- Adding `due_date: Optional[date] = None` to `TaskCreate`
- Adding `due_date: Optional[date] = None` to `TaskUpdate`
- Adding `due_date: Optional[date] = None` to `TaskResponse`
- Relying on Pydantic's built-in parsing and serialization

#### AI response summary

Copilot added the optional date field to all three task models without adding custom validators or modifying the API routes, storage functions, tests, or frontend.

#### Decision

Accepted:
- Python's built-in `date` type
- The optional field in all three task models
- Pydantic's built-in YYYY-MM-DD parsing
- Keeping the existing generic storage creation and update behavior

Edited:
- No code edits were required after reviewing the focused model change

Rejected:
- No custom validator or extra storage logic was added because the existing behavior already supported the field

Process note:
- Copilot again applied the change before waiting for approval, despite the instruction to show the diff first

Reason:
The minimal model-only change made all create, response, update, and removal tests pass while preserving the existing architecture.

### Prompt 4 — Add invalid-date and overdue-filter tests

#### Prompt summary

Copilot was asked to add exactly four focused backend tests:

- Invalid due date returns HTTP 422
- `overdue=true` returns only unfinished past-due tasks
- `overdue=false` behaves like no filter
- Overdue filtering combines with search, status, and priority

The tests used relative dates based on `date.today()` and valid task-status transitions.

#### AI response summary

Copilot added the four requested tests to `tests/test_tasks.py`.

The combined-filter test created controlled tasks so that search, status, priority, and overdue filtering were each necessary to isolate the expected result.

#### Decision

Accepted:
- The invalid-date validation test
- The unfinished past-due filtering test
- The defined `overdue=false` behavior
- The combined-filter test structure
- Relative dates using `date.today()` and `timedelta`
- Valid task-status transitions

Edited:
- Corrected spacing in the `client: TestClient` type annotation

Rejected:
- No test logic was rejected because each scenario was focused and every filter was necessary

Process note:
- Copilot applied the tests before waiting for approval, despite being asked to show the diff first

Reason:
The tests clearly define the remaining backend behavior without relying on fixed calendar dates.


### Prompt 5 — Implement backend overdue filtering

#### Prompt summary

Copilot was asked to make the smallest backend change required to pass the two failing `overdue=true` tests.

The requested implementation was limited to:

- Adding `overdue: Optional[bool] = None` to the existing `GET /tasks` route
- Passing overdue into `storage.get_all_tasks`
- Applying overdue-only filtering only when overdue is explicitly true
- Defining overdue as a due date before today and status not Done
- Preserving combinations with search, status, and priority

#### AI response summary

Copilot added the optional overdue query parameter to `app/main.py` and added overdue filtering to `app/storage.py`.

Its first version compared the task status using object identity:

`task.status is not TaskStatus.DONE`

#### Decision

Accepted:
- Extending the existing list endpoint instead of creating a new endpoint
- Passing the optional boolean into storage
- Filtering only when overdue is true
- Comparing due dates against `date.today()`
- Combining overdue with the existing filters

Edited:
- Changed `task.status is not TaskStatus.DONE` to `task.status != TaskStatus.DONE` so the code clearly compares enum values rather than object identity

Rejected:
- No broader refactor or unrelated backend changes were accepted

Process note:
- Copilot applied the initial changes before waiting for approval, despite being asked to show the diff first

Reason:
The implementation was focused and correct after the status comparison was reviewed and improved.
