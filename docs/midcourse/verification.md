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

### Feature 1 frontend manual verification

The frontend filter toolbar was tested manually with four controlled tasks:

- Alpha Report — High, ToDo
- Alpha Cleanup — Low, ToDo
- Beta Report — High, ToDo
- Alpha Done — High, Done

The following checks passed:

1. Searching `alpha` displayed Alpha Report, Alpha Cleanup, and Alpha Done while excluding Beta Report.
2. Selecting High priority displayed Alpha Report, Beta Report, and Alpha Done while excluding Alpha Cleanup.
3. Combining search `alpha` with High priority displayed only Alpha Report and Alpha Done.
4. Searching `quarterly` matched Alpha Report and Beta Report through their descriptions.
5. A no-match search displayed no task cards, returned no application error, and preserved all three empty Kanban columns.
6. Clear Filters reset both controls and restored all four tasks.
7. Active filters remained applied after editing Alpha Report.
8. Active filters remained applied after an invalid Done to ToDo drag.
9. The invalid drag was rejected, the card returned to Done, and unrelated filtered-out tasks did not reappear.

The existing task modal, priority ordering, valid status transitions, invalid transition rollback, and three-column board layout continued to work.

### Break Test 1 — Backend search filtering

Protected test:

`test_list_tasks_search_matches_title_case_insensitively`

Deliberate break:

The search condition in `storage.get_all_tasks` was temporarily disabled by changing it so the search block could not execute.

Command:

`python3 -m pytest tests/test_tasks.py -k "test_list_tasks_search_matches_title_case_insensitively" -q`

Failure result:

`1 failed, 20 deselected`

Important failure evidence:

`AssertionError: assert 2 == 1`

The API returned both the matching and non-matching tasks because search filtering was disabled. This proved that the test detects broken search behavior.

Restoration:

The committed working version of `app/storage.py` was restored.

Targeted result after restoration:

`1 passed, 20 deselected`

Full-suite result after restoration:

`21 passed, 1 warning`

Conclusion:

The search regression test successfully failed when the protected behavior was broken and passed again after the implementation was restored.

## Feature 2 — Due Dates and Overdue Filtering

### Initial due-date test-first red phase

Three due-date tests were added before implementation:

- `test_create_task_with_valid_due_date_returns_201_and_exposes_due_date`
- `test_create_task_without_due_date_returns_none`
- `test_patch_task_due_date_can_add_change_and_remove`

Command:

`python3 -m pytest tests/test_tasks.py -k "due_date" -q`

Result:

`3 failed, 21 deselected`

Observed failures:

- Valid due-date creation returned HTTP 422 instead of 201
- A normal task response did not contain the `due_date` key
- PATCH with a due date returned HTTP 422 instead of 200

These were the expected failures because the task models did not yet define the optional due-date field.

### Initial due-date implementation — green phase

The optional `due_date` field was added to:

- `TaskCreate`
- `TaskUpdate`
- `TaskResponse`

Python's `date` type and Pydantic's built-in date parsing were used. No custom validator or special storage code was required.

Targeted command:

`python3 -m pytest tests/test_tasks.py -k "due_date" -q`

Result:

`3 passed, 21 deselected`

Full-suite command:

`python3 -m pytest tests -q`

Result:

`24 passed, 1 warning`

The existing generic creation and partial-update logic successfully supported adding, changing, and removing due dates.
