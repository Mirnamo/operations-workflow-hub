from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum
from pydantic import BaseModel, Field


class Status(StrEnum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETE = "complete"


class Priority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class WorkItemCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    owner: str = Field(min_length=2, max_length=80)
    priority: Priority = Priority.MEDIUM
    due_date: date | None = None


class WorkItem(WorkItemCreate):
    id: int
    status: Status = Status.NEW
    created_at: datetime


class WorkItemPatch(BaseModel):
    owner: str | None = Field(default=None, min_length=2, max_length=80)
    priority: Priority | None = None
    status: Status | None = None
    due_date: date | None = None


class AuditEvent(BaseModel):
    id: int
    item_id: int
    actor: str
    action: str
    occurred_at: datetime
