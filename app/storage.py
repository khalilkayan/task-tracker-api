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
    task = TaskResponse(**payload.model_dump())
    _tasks[task.id] = task
    return task


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    q: Optional[str] = None,
    overdue: Optional[bool] = None,
) -> list[TaskResponse]:
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
    return _tasks.get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    existing_task = _tasks.get(task_id)
    if existing_task is None:
        return None

    updates = payload.model_dump(exclude_unset=True)
    updates["updated_at"] = datetime.now(timezone.utc)
    updated_task = existing_task.model_copy(update=updates)
    _tasks[task_id] = updated_task
    return updated_task


def delete_task(task_id: str) -> bool:
    if task_id in _tasks:
        del _tasks[task_id]
        return True
    return False


def _reset() -> None:
    _tasks.clear()
