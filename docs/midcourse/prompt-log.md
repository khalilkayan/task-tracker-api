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
