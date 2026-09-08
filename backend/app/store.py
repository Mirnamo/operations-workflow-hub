from __future__ import annotations

from datetime import date, datetime, timezone
from threading import Lock
from .models import AuditEvent, Priority, Status, WorkItem, WorkItemCreate, WorkItemPatch


class Store:
    def __init__(self) -> None:
        self._lock = Lock()
        now = datetime.now(timezone.utc)
        self.items = [
            WorkItem(id=1, title="Validate vendor import", owner="Merna", priority=Priority.HIGH, status=Status.IN_PROGRESS, due_date=date.today(), created_at=now),
            WorkItem(id=2, title="Review access request", owner="Operations", priority=Priority.MEDIUM, status=Status.NEW, created_at=now),
            WorkItem(id=3, title="Resolve failed integration", owner="Platform", priority=Priority.URGENT, status=Status.BLOCKED, created_at=now),
        ]
        self.events: list[AuditEvent] = []

    def create(self, data: WorkItemCreate, actor: str) -> WorkItem:
        with self._lock:
            item = WorkItem(id=max((x.id for x in self.items), default=0) + 1, created_at=datetime.now(timezone.utc), **data.model_dump())
            self.items.append(item)
            self._audit(item.id, actor, "created")
            return item

    def update(self, item_id: int, data: WorkItemPatch, actor: str) -> WorkItem | None:
        with self._lock:
            for index, item in enumerate(self.items):
                if item.id == item_id:
                    updated = item.model_copy(update=data.model_dump(exclude_none=True))
                    self.items[index] = updated
                    self._audit(item_id, actor, "updated")
                    return updated
        return None

    def _audit(self, item_id: int, actor: str, action: str) -> None:
        self.events.append(AuditEvent(id=len(self.events) + 1, item_id=item_id, actor=actor, action=action, occurred_at=datetime.now(timezone.utc)))
