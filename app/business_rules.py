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
    """Validate that a task status transition is allowed.

    Args:
        current: The task's current status.
        new: The requested new status.

    Returns:
        None: If (current, new) is a member of VALID_TRANSITIONS.

    Raises:
        HTTPException: With status code 422 if (current, new) is not a
            member of VALID_TRANSITIONS. The detail includes the current
            status, the requested new status, and the allowed transitions.
    """
    if (current, new) in VALID_TRANSITIONS:
        return

    allowed = ", ".join(
        f"{start.value}->{end.value}" for start, end in sorted(VALID_TRANSITIONS, key=lambda item: (item[0].value, item[1].value))
    )
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=f"Invalid status transition from {current.value} to {new.value}. Allowed transitions: {allowed}",
    )
