from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app import storage
from app.business_rules import validate_status_transition
from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate


app = FastAPI(
    title="Task Tracker API",
    description="A minimal FastAPI skeleton for the Task Tracker learning project.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5173",
        "null",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str
    timestamp: str


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Report basic service liveness.

    Returns:
        HealthResponse: status "ok" and the current UTC timestamp,
        returned with the default HTTP 200 status.

    Example:
        GET /health -> 200
        {"status": "ok", "timestamp": "<current UTC ISO 8601 timestamp>"}
    """
    return HealthResponse(
        status="ok",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    """Create a new task.

    Args:
        payload: The task creation data.

    Returns:
        TaskResponse: The newly created and stored task, returned with
        HTTP 201.

    Example:
        POST /tasks {"title": "Buy milk"} -> 201
        A TaskResponse representing the newly created task.
    """
    return storage.add_task(payload)


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    q: Optional[str] = None,
    overdue: Optional[bool] = None,
) -> list[TaskResponse]:
    """List tasks, optionally filtered by status, priority, search text, and overdue state.

    Args:
        status: If provided, only include tasks with this exact status.
        priority: If provided, only include tasks with this exact
            priority.
        q: If provided and non-blank after stripping, only include tasks
            whose title or description contains this text as a
            case-insensitive substring.
        overdue: If True, only include tasks that are overdue (due_date
            earlier than today and status other than Done).

    Returns:
        list[TaskResponse]: The tasks returned by storage.get_all_tasks
        after applying all supplied filters (combined with AND
        semantics), returned with the default HTTP 200 status. An empty
        list if nothing matches.

    Example:
        GET /tasks?q=milk&priority=High -> 200
        A list of matching TaskResponse objects, or [] if none match.
    """
    return storage.get_all_tasks(status=status, priority=priority, q=q, overdue=overdue)


@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["tasks"],
    responses={404: {"description": "Task not found"}},
)
def get_task(task_id: str) -> TaskResponse:
    """Retrieve a single task by its id.

    Args:
        task_id: The id of the task to retrieve.

    Returns:
        TaskResponse: The matching task, returned with the default HTTP
        200 status.

    Raises:
        HTTPException: With status code 404 if no task with the given
            task_id exists.

    Example:
        GET /tasks/{task_id} -> 200
        A TaskResponse for the given task_id, or 404 if it does not
        exist.
    """
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@app.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["tasks"],
    responses={
        404: {"description": "Task not found"},
        422: {
            "description": (
                "Validation error: either the request body failed schema "
                "validation, or payload.status was supplied and the "
                "requested transition from the task's current status is "
                "not allowed."
            ),
            "content": {
                "application/json": {
                    "schema": {
                        "oneOf": [
                            {"$ref": "#/components/schemas/HTTPValidationError"},
                            {
                                "type": "object",
                                "required": ["detail"],
                                "properties": {
                                    "detail": {"type": "string"},
                                },
                            },
                        ]
                    }
                }
            },
        },
    },
)
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    """Apply a partial update to an existing task.

    Args:
        task_id: The id of the task to update.
        payload: The fields to update. Only fields explicitly set on the
            payload are applied to the existing task.

    Returns:
        TaskResponse: The updated task, returned with the default HTTP
        200 status.

    Raises:
        HTTPException: With status code 404 if no task with the given
            task_id exists.
        HTTPException: With status code 422, propagated from
            validate_status_transition, only when payload.status is
            supplied and the transition from the task's current status
            to the requested status is not allowed. This is distinct
            from any 422 response FastAPI/Pydantic may return for a
            malformed request body, which is not raised by this
            function.

    Example:
        PATCH /tasks/{task_id} {"status": "InProgress"} -> 200
        The updated TaskResponse, 404 if task_id does not exist, or 422
        if the requested status transition is not allowed.
    """
    if payload.status is not None:
        existing_task = storage.get_task_by_id(task_id)
        if existing_task is None:
            raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
        validate_status_transition(existing_task.status, payload.status)

    updated_task = storage.update_task(task_id, payload)
    if updated_task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return updated_task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["tasks"],
    responses={404: {"description": "Task not found"}},
)
def delete_task(task_id: str) -> None:
    """Delete a task by its id.

    Args:
        task_id: The id of the task to delete.

    Returns:
        None: No response body, returned with HTTP 204 after successful
        deletion.

    Raises:
        HTTPException: With status code 404 if no task with the given
            task_id exists.

    Example:
        DELETE /tasks/{task_id} -> 204 (no body), or 404 if task_id does
        not exist.
    """
    deleted = storage.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
