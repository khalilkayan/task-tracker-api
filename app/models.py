from datetime import date, datetime, timezone
from enum import Enum
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    description: Optional[str] = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    due_date: Optional[date] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        """Validate and normalize a task title.

        Args:
            value: The raw title string to validate.

        Returns:
            str: The stripped title.

        Raises:
            ValueError: If the stripped title is empty.
            ValueError: If the stripped title exceeds 200 characters.
        """
        stripped_title = value.strip()
        if not stripped_title:
            raise ValueError("title cannot be empty")
        if len(stripped_title) > 200:
            raise ValueError("title cannot exceed 200 characters")
        return stripped_title


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    due_date: Optional[date] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: Optional[str]) -> str:
        """Validate and normalize an optional task title.

        Args:
            value: The raw title string to validate, or None.

        Returns:
            str: The stripped title.

        Raises:
            ValueError: If value is None.
            ValueError: If the stripped title is empty.
            ValueError: If the stripped title exceeds 200 characters.
        """
        if value is None:
            raise ValueError("title cannot be null")

        stripped_title = value.strip()
        if not stripped_title:
            raise ValueError("title cannot be empty")
        if len(stripped_title) > 200:
            raise ValueError("title cannot exceed 200 characters")
        return stripped_title


class TaskResponse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    description: Optional[str] = ""
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str] = None
    due_date: Optional[date] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
