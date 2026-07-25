# Mini Architecture Decision Record

## Project

AI-Assisted Feature Extension Sprint

## Status

Accepted before implementation

## Context

The existing Task Tracker includes a FastAPI backend, in-memory task storage, pytest tests, and a vanilla HTML, CSS, and JavaScript Kanban frontend.

The mid-course project requires two small end-to-end features. Each feature must demonstrate planning, constrained AI prompting, code review, testing, debugging, refactoring, and documentation.

The selected features are:

1. Search and combined filters
2. Due dates and overdue filtering

These features were selected because they extend the existing Task Tracker without requiring a new framework, database, authentication system, or separate application page.

---

## Decision 1 — Search and combined filters

The existing `GET /tasks` endpoint will be extended instead of creating a separate search endpoint.

An optional `q` query parameter will search task titles and descriptions.

Search behavior will be:

- Case-insensitive
- Based on partial text matches
- Applied to both title and description
- Combinable with priority and other supported filters
- Returned as HTTP 200 with an empty list when nothing matches

The frontend will contain a compact toolbar above the Kanban board with:

- A search input
- A priority filter
- A Clear Filters control

The existing ToDo, InProgress, and Done columns will remain visible while filtering.

### Alternatives considered and rejected

#### Separate search endpoint

A separate endpoint such as `/tasks/search` was rejected because extending `GET /tasks` is simpler and keeps task retrieval and filtering in one place.

#### Frontend-only filtering

Filtering only the tasks already loaded in the browser was rejected because the project should demonstrate backend query handling and backend tests.

#### Separate search-results page

A separate results page was rejected because it would duplicate the existing Kanban interface and increase frontend scope.

#### Saved searches, pagination, and advanced sorting

These were rejected because they are not required for the selected feature and would make the sprint unnecessarily large.

---

## Decision 2 — Due dates and overdue filtering

Tasks will receive an optional `due_date` field.

The field will use a date-only value in the format:

`YYYY-MM-DD`

It will be supported during:

- Task creation
- Task updates
- Task responses

A task will be considered overdue only when:

1. It has a due date.
2. Its due date is before the current date.
3. Its status is not Done.

Overdue status will be determined using backend logic so that API filtering and frontend display use one consistent rule.

The existing `GET /tasks` endpoint will support an optional overdue filter.

The frontend will add:

- An optional due-date input to the Create/Edit modal
- Due-date text on task cards
- An Overdue indicator for overdue unfinished tasks
- An Overdue Only filter above the board

### Alternatives considered and rejected

#### Date and time values

Datetime values were rejected because the project only needs calendar dates. Adding times and time zones would introduce unnecessary complexity.

#### Frontend-only overdue calculation

Calculating overdue status only in the browser was rejected because backend filtering also needs a consistent overdue rule that can be tested with pytest.

#### Notifications and reminders

Notifications, reminder emails, and scheduled alerts were rejected because they would require additional infrastructure and are outside the selected feature scope.

#### Calendar libraries or widgets

A calendar library was rejected because the browser's standard date input is sufficient for this project.

---

## Shared implementation constraints

The implementation will preserve the existing architecture:

- FastAPI backend
- Existing in-memory storage
- Existing Pydantic models
- Vanilla HTML, CSS, and JavaScript frontend
- Existing pytest structure

The implementation will not introduce:

- React or another frontend framework
- A database
- Authentication
- External notification services
- New deployment infrastructure
- Unrelated design changes

Each feature will be implemented in small steps:

1. Backend behavior
2. Targeted tests
3. Full test suite
4. Frontend integration
5. Manual browser verification
6. Break Test
7. Focused refactor
8. Final verification
