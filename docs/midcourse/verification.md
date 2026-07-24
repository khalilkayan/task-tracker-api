# Verification Log

## Baseline Check

Date: 23 July 2026

### Automated tests

Command: `python3 -m pytest tests -q`

Result: 16 passed, 1 warning in 0.03s.

The warning was a FastAPI deprecation warning involving `HTTP_422_UNPROCESSABLE_ENTITY`. It did not cause a test failure.

### Backend checks

- `GET /health` opened successfully.
- FastAPI Swagger documentation opened at `/docs`.
- The existing backend DELETE endpoint returned HTTP 204.

### Frontend checks

- The Kanban board loaded successfully.
- All three columns were visible: ToDo, InProgress, and Done.
- A new task could be created.
- An existing task could be edited.
- A task could move from ToDo to InProgress.
- A task could move from InProgress to Done.
- An invalid Done to ToDo transition was rejected and rolled back.
- The frontend did not include a delete button before the project began.

### Baseline conclusion

The original Task Tracker was working before the two mid-course features were added.

## Feature 1 — Search and Combined Filters

### Test-first red phase

Two search tests were added before implementing backend search:

- `test_list_tasks_search_matches_title_case_insensitively`
- `test_list_tasks_search_matches_description_case_insensitively`

Command:

`python3 -m pytest tests/test_tasks.py -q`

Result:

`2 failed, 16 passed, 1 warning`

The failures occurred because `GET /tasks` did not yet apply the `q` search parameter and returned both the matching and non-matching tasks. This was the expected result before implementation.

### Backend search implementation — green phase

The existing `GET /tasks` endpoint was extended with an optional `q` parameter.

Search behavior implemented:

- Searches task title and description.
- Uses case-insensitive partial matching.
- Treats missing, empty, or whitespace-only search as no filter.
- Continues to combine with existing status and priority filters.
- Safely handles tasks whose description is null.

Targeted command:

`python3 -m pytest tests/test_tasks.py -k "search" -q`

Result:

`2 passed, 16 deselected`

Full-suite command:

`python3 -m pytest tests -q`

Result:

`18 passed, 1 warning in 0.04s`

The original 16 tests remained passing after backend search was added.

### Additional Feature 1 backend coverage

Three additional tests were added:

- `test_list_tasks_whitespace_search_behaves_like_no_filter`
- `test_list_tasks_search_no_match_returns_200_and_empty_list`
- `test_list_tasks_search_combines_with_status_and_priority`

The combined-filter test includes two High-priority InProgress tasks, but only one contains the search text. This proves that the search filter is required in addition to status and priority.

Targeted result:

`3 passed`

Full-suite result:

`21 passed, 1 warning`

All original tests and all new search tests passed.
