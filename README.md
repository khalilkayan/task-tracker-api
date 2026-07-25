# Task Tracker API

A small full-stack task-management project built with FastAPI, in-memory Python storage, pytest, and a vanilla HTML, CSS, and JavaScript Kanban board.

This mid-course extension adds two end-to-end features:

1. Search and combined task filters
2. Due dates and overdue filtering

## Features

- Create, read, update, and delete tasks
- ToDo, InProgress, and Done Kanban columns
- Validated task-status transitions
- Search by task title or description
- Filter by priority
- Combine search, priority, and overdue filters
- Add, change, or remove optional due dates
- Display due dates and Overdue indicators on task cards
- Filter for unfinished overdue tasks
- Responsive vanilla JavaScript frontend
- Automated API tests with pytest

## Technology

- Python
- FastAPI
- Pydantic
- pytest
- HTML
- CSS
- JavaScript

## Project structure

```text
app/
├── frontend/
│   └── index.html
├── business_rules.py
├── main.py
├── models.py
└── storage.py

docs/
└── midcourse/
    ├── mini-adr.md
    ├── prompt-log.md
    ├── reflection.md
    ├── user-stories.md
    └── verification.md

tests/
└── test_tasks.py
cat > README.md <<'EOF'
# Task Tracker API

A small full-stack task-management project built with FastAPI, in-memory Python storage, pytest, and a vanilla HTML, CSS, and JavaScript Kanban board.

This mid-course extension adds two end-to-end features:

1. Search and combined task filters
2. Due dates and overdue filtering

## Features

- Create, read, update, and delete tasks
- ToDo, InProgress, and Done Kanban columns
- Validated task-status transitions
- Search by task title or description
- Filter by priority
- Combine search, priority, and overdue filters
- Add, change, or remove optional due dates
- Display due dates and Overdue indicators on task cards
- Filter for unfinished overdue tasks
- Responsive vanilla JavaScript frontend
- Automated API tests with pytest

## Technology

- Python
- FastAPI
- Pydantic
- pytest
- HTML
- CSS
- JavaScript

## Project structure

```text
app/
├── frontend/
│   └── index.html
├── business_rules.py
├── main.py
├── models.py
└── storage.py

docs/
└── midcourse/
    ├── mini-adr.md
    ├── prompt-log.md
    ├── reflection.md
    ├── user-stories.md
    └── verification.md

tests/
└── test_tasks.py
