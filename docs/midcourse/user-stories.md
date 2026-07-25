# Mid-Course Project User Stories

## Feature 1: Search and Combined Filters

### User Story 1 — Search by task text

As a user, I want to search tasks by title or description so that I can quickly find relevant work.

#### Acceptance criteria

- A search input is visible above the Kanban board.
- Search is case-insensitive.
- Partial matches are accepted.
- Both the task title and description are searched.
- A search with no matches does not produce an application error.
- A search with no matches returns HTTP 200 with an empty task list.

### User Story 2 — Filter by priority

As a user, I want to filter tasks by priority so that I can focus on the most important work.

#### Acceptance criteria

- A priority filter is visible above the board.
- The user can choose High, Medium, Low, or All.
- Only tasks matching the selected priority are displayed.
- Selecting All displays tasks of every priority.
- The three Kanban columns remain visible while filtering.

### User Story 3 — Combine search and filters

As a user, I want search and priority filtering to work together so that I can narrow the board more precisely.

#### Acceptance criteria

- Search text and priority can be active at the same time.
- A task is displayed only when it satisfies all active filters.
- Clearing the search does not automatically clear the priority filter.
- A Clear Filters control resets all active search and filter values.
- Empty columns display their existing empty state instead of disappearing.

### User Story 4 — Preserve existing board behavior

As a user, I want filtered tasks to keep their normal Kanban behavior so that searching does not break task management.

#### Acceptance criteria

- The board still contains ToDo, InProgress, and Done columns.
- Task cards retain their existing priority sorting.
- Existing create and edit behavior continues to work.
- Existing valid and invalid status-transition rules continue to work.
- Existing tasks are not modified or deleted by using the filters.

### AI assumption corrected for Feature 1

During planning, AI suggested patterns that could have produced a separate results list or hidden empty columns. I kept the existing three-column Kanban board visible because the project brief specifically asks for a compact filter area while preserving board and empty-column states. I also rejected saved searches, pagination, and a separate search page as unnecessary scope.

---

## Feature 2: Due Dates and Overdue Filtering

### User Story 1 — Add an optional due date

As a user, I want to assign an optional due date when creating a task so that I know when it should be completed.

#### Acceptance criteria

- The Create Task modal contains an optional due-date field.
- The field uses the date format YYYY-MM-DD.
- A task can still be created without a due date.
- A valid due date is stored and returned by the API.
- An invalid date value is rejected with HTTP 422.

### User Story 2 — Edit a due date

As a user, I want to add, change, or remove a task's due date so that the task remains accurate when plans change.

#### Acceptance criteria

- The Edit Task modal displays the task's current due date.
- The due date can be changed.
- The due date can be added to a task that previously had none.
- The due date can be removed.
- Updating only the due date does not change unrelated task fields.

### User Story 3 — See due dates and overdue status

As a user, I want to see due dates on task cards and clearly identify overdue tasks.

#### Acceptance criteria

- A task card displays its due date when one exists.
- Tasks without a due date do not display an empty or misleading date.
- A task is overdue when its due date is before the current date and its status is not Done.
- Overdue unfinished tasks display an Overdue indicator.
- Completed tasks do not display as overdue, even when their due date is in the past.

### User Story 4 — Filter overdue tasks

As a user, I want to display only overdue tasks so that I can focus on unfinished work that is late.

#### Acceptance criteria

- An Overdue Only filter is visible above the board.
- Enabling the filter displays only overdue unfinished tasks.
- Tasks with future due dates are excluded.
- Tasks without due dates are excluded.
- Completed tasks are excluded.
- The overdue filter can be combined with search and priority filtering.

### AI assumption corrected for Feature 2

During planning, AI could have expanded due dates into date-and-time values, reminders, notifications, calendar widgets, or time-zone handling. I limited the feature to an optional date-only value because the assignment asks for a small end-to-end feature. Overdue status will be determined consistently using the rule: due date before today and status not Done.
