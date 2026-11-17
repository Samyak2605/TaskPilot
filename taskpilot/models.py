"""Validated application data models."""

from datetime import date
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(BaseModel):
    """A student task. Missing fields remain missing; they are never guessed."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str = Field(min_length=1, max_length=160)
    description: str | None = Field(default=None, max_length=1000)
    due_date: date | None = None
    estimated_minutes: int | None = Field(default=None, ge=1, le=1440)
    priority: Priority = Priority.MEDIUM
    urgency_score: int | None = Field(default=None, ge=0, le=115)
    priority_reason: str | None = Field(default=None, max_length=500)

    @field_validator("title")
    @classmethod
    def strip_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Task title cannot be blank")
        return value

    @field_validator("description")
    @classmethod
    def strip_description(cls, value: str | None) -> str | None:
        return value.strip() if value and value.strip() else None


class MissingDetail(BaseModel):
    task_id: str
    task_title: str
    field: str
    message: str


class RankedTask(BaseModel):
    task: Task
    score: int
    explanation: str
    warnings: list[MissingDetail] = Field(default_factory=list)


class AgentResult(BaseModel):
    checklist: list[RankedTask]
    final_message: str
    activity: list[dict]
    stopped_at_limit: bool = False

