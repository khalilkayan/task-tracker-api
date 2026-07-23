from fastapi import HTTPException, status

from app.models import TaskStatus


VALID_TRANSITIONS: frozenset[tuple[TaskStatus, TaskStatus]] = frozenset(
    {
        (TaskStatus.TODO, TaskStatus.IN_PROGRESS),
        (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
        (TaskStatus.DONE, TaskStatus.IN_PROGRESS),
    }
)


def validate_status_transition(current: TaskStatus, new: TaskStatus) -> None:
    if (current, new) in VALID_TRANSITIONS:
        return

    allowed = ", ".join(
        f"{start.value}->{end.value}" for start, end in sorted(VALID_TRANSITIONS, key=lambda item: (item[0].value, item[1].value))
    )
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=f"Invalid status transition from {current.value} to {new.value}. Allowed transitions: {allowed}",
    )
