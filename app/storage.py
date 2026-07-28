from datetime import date, datetime, timezone
from typing import Optional

from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate


_tasks: dict[str, TaskResponse] = {}


def _is_task_overdue(task: TaskResponse, today: date) -> bool:
    return (
        task.due_date is not None
        and task.due_date < today
        and task.status != TaskStatus.DONE
    )


def add_task(payload: TaskCreate) -> TaskResponse:
    """Create and store a new task.

    Args:
        payload: The task creation data.

    Returns:
        TaskResponse: The newly created task, generated from payload and
        stored in the in-memory task store.
    """
    task = TaskResponse(**payload.model_dump())
    _tasks[task.id] = task
    return task


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    q: Optional[str] = None,
    overdue: Optional[bool] = None,
) -> list[TaskResponse]:
    """List tasks, optionally filtered by search text, status, priority, and overdue state.

    Args:
        status: If provided, only include tasks with this exact status.
        priority: If provided, only include tasks with this exact priority.
        q: If provided and non-blank after stripping, only include tasks
            whose title or description contains this text as a
            case-insensitive substring (using casefold comparison). A
            None or blank/whitespace-only value applies no text filtering.
        overdue: If True, only include tasks that are overdue (have a
            due_date earlier than today and a status other than Done).
            Any other value (None or False) applies no overdue filtering.

    Returns:
        list[TaskResponse]: The tasks matching all supplied filters,
        combined with AND semantics. An empty list if none match.
    """
    tasks = list(_tasks.values())

    if q is not None:
        query = q.strip().casefold()
        if query:
            tasks = [
                task
                for task in tasks
                if query in task.title.casefold()
                or query in (task.description or "").casefold()
            ]

    if status is not None:
        tasks = [task for task in tasks if task.status == status]

    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]

    if overdue is True:
        today = date.today()
        tasks = [task for task in tasks if _is_task_overdue(task, today)]

    return tasks


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    """Retrieve a single task by its id.

    Args:
        task_id: The id of the task to retrieve.

    Returns:
        Optional[TaskResponse]: The matching task, or None if no task with
        that id exists.
    """
    return _tasks.get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    """Apply a partial update to an existing task.

    Args:
        task_id: The id of the task to update.
        payload: The fields to update. Only fields explicitly set on the
            payload are applied; unset fields leave the existing value
            unchanged.

    Returns:
        Optional[TaskResponse]: The updated task with a refreshed
        updated_at timestamp, or None if no task with that id exists.
    """
    existing_task = _tasks.get(task_id)
    if existing_task is None:
        return None

    updates = payload.model_dump(exclude_unset=True)
    updates["updated_at"] = datetime.now(timezone.utc)
    updated_task = existing_task.model_copy(update=updates)
    _tasks[task_id] = updated_task
    return updated_task


def delete_task(task_id: str) -> bool:
    """Delete a task by its id.

    Args:
        task_id: The id of the task to delete.

    Returns:
        bool: True if a task with that id existed and was deleted, False
        if no task with that id exists.
    """
    if task_id in _tasks:
        del _tasks[task_id]
        return True
    return False


def _reset() -> None:
    _tasks.clear()
